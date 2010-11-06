#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""El tarificador se encarga de establecer las reglas de negocio para
dar un precio final.

El precio del contrato es únicamente una referencia, ya que dicho precio se puede modificar
a voluntad dentro del inventario y a la postre es el precio que vale

"""
from django.db.models import Q
from motor.models import Inventario
from motor.models import RestriccionOcupacion
from motor.models import RestriccionBlackout
from motor.models import RestriccionEstanciaMinima
from motor.models import SuplementoOcupacion
from motor.models import DescuentoNin
from motor.models import SuplementoDia
from motor.models import SuplementoRegimen
from motor.core.interval import datetime_iterator
import datetime
import logging
log = logging.getLogger(__name__)

class Info(object):
    """Información de la dipsonibilidad: fecha, cupo
    etc. Para ser usado junto con Habitacion"""

    def __init__(self, fecha, cupo, precio,
                 is_apartamento, contrato):
        self.fecha = fecha
        self.cupo = cupo
        self.precio_base = precio
        self.precio_adultos = None
        self.dto_ninyos = 0
        self.is_apartamento = is_apartamento
        self.contrato = contrato

    def add_dto_ninyos(self, value):
        self.dto_ninyos = value

class Habitacion(object):
    """Definición de la habitación, para ser usada
    junto con Hotel"""

    def __init__(self, tipo, regimen, hotel):
        self.tipo = tipo
        self.regimen = regimen
        self.inventario = []
        self.consulta = hotel.consulta
        self._contratos = None
        self.hotel = hotel
        self.slug = "%s-%s" % (self.tipo.slug, self.regimen.slug)
        self._restricciones = {}

    def __str__(self):
        return self.slug

    @property
    def contratos(self, refresh=False):
        if not self._contratos or refresh:
            self._contratos = list(set(x.contrato for x in  self.inventario))
        return self._contratos

    def add_inventario(self, value):
        self.inventario.append(value)

    @property
    def precio(self):
        adultos = sum(x.precio_adultos for x in self.inventario)*self.consulta.adultos
        if self.consulta.ninyos > 0:
            ninyos = sum(x.precio_adultos*(self.consulta.ninyos-x.dto_ninyos) for x in self.inventario)
            total = adultos + ninyos
        else:
            total = adultos
        total += self._calcular_suplemento_dia()
        return total

    def _calcular_suplemento_dia(self):
        "Calcula los suplementos que hay que aplicar"
        total = 0
        for suplemento in self.hotel.get_suplementos_dia():
            log.debug('Aplicando el suplemento %s' % suplemento)
            if suplemento.aplicabilidad in ['A','T']:
                total += suplemento.precio*self.consulta.adultos
            elif suplemenot.aplicabilidad in ['N','T']:
                total += suplemento.precio*self.consulta.ninyos
        return total

    def _sin_restriccion_estancia_minima(self):
        """Comprueba que el número de noches cumple la restricción de
        estancia mínima"""
        if self._restricciones.get('estancia_minima',False):
            log.debug('La habitación ya tiene restricciones de estancia mínima')
            return False
        for contrato in self.contratos:
            log.debug('Comprobando restricciones de estancia mínima')
            num_noches = self.consulta.noches
            hay_restriccion  = RestriccionEstanciaMinima.objects. \
                    filter(contrato__id=contrato.pk). \
                    filter(Q(minimo_noches__gt=num_noches)|Q(maximo_noches__lt=num_noches)). \
                    exclude(Q(fecha_inicio__gt=self.consulta.fin)|Q(fecha_fin__lt=self.consulta.inicio))
            if len(hay_restriccion)>0:
                self._restricciones['estancia_minima'] = True
                log.debug('Encontrada restricción de estancia mínima')
                return False
        return True


    def _sin_restriccion_blackout(self):
        """Comprueba que la fecha de la reserva (hoy) es mayor que la fecha de entrada en
        un número de días especificado por el valor del blackout"""

        if self._restricciones.get('blackout', False):
            log.debug('La habitación ya tiene restricciones de blackout')
            return False
        fecha = datetime.date.today()
        for contrato in self.contratos:
            log.debug('Comprobando restricciones de blackout')
            condiciones  = RestriccionBlackout.objects. \
                    filter(contrato__id=contrato.pk). \
                    exclude(Q(fecha_inicio__gt=self.consulta.fin)|Q(fecha_fin__lt=self.consulta.inicio))
            for restriccion in condiciones:
                if fecha >= self.consulta.inicio + datetime.timedelta(days=-restriccion.minimo_dias):
                    self._restricciones['blackout'] = True
                    log.debug('Encontrada restricción de blackout')
                    return False
        return True


    def _sin_restriccion_ocupacion(self):
        """Comprueba si hay restricciones adicionales a la ocupación
        para esas fechas"""
        if self._restricciones.get('ocupacion', False):
            log.debug('La habitación ya tiene restricciones')
            return False
        for contrato in self.contratos:
            log.debug('Comprobando restricciones para %s' % self.tipo)
            condiciones  = RestriccionOcupacion.objects. \
                    filter(contrato__id=contrato.pk, tipo_habitacion__id = self.tipo.pk). \
                    exclude(Q(fecha_inicio__gt=self.consulta.fin)|Q(fecha_fin__lt=self.consulta.inicio))
            for restriccion in condiciones:
                if restriccion.is_restriccion(self.consulta.adultos, self.consulta.ninyos):
                    self._restricciones['ocupacion'] = True
                    log.debug('Encontrada restricción de ocupación: %s' % restriccion.id)
                    return False
        return True

    def is_valid(self):
        valor = (len(self.inventario)==self.consulta.noches) \
            and self.tipo.is_valid(self.consulta.adultos,self.consulta.ninyos) \
            and self._sin_restriccion_ocupacion() \
            and self._sin_restriccion_blackout()  \
            and self._sin_restriccion_estancia_minima()
        return valor


class Hotel(object):
    """
    Clase que contiene el hotel obtenido en la disponibilidad.
    Para ser usado junto con Disponibilidad
    """
    def __init__(self, hotel, disponibilidad):
        self.model = hotel
        self.slug = hotel.slug
        self._habitaciones = {}
        self._contratos = set()
        self._cleaned = False
        self.consulta = disponibilidad.consulta
        self._cache_precio = {}
        self.suplementos_regimen = {}
        self.disponiblidad=disponibilidad

    def add_habitacion(self, habitacion):
        if not habitacion.slug in self._habitaciones:
            self._habitaciones[habitacion.slug] = habitacion
        return  self._habitaciones[habitacion.slug]

    def get_suplementos_dia(self):
        if not hasattr(self, '_suplementos_dia'):
            supl = SuplementoDia.objects.filter(fecha__gte=self.consulta.inicio,
                                            fecha__lte=self.consulta.fin,
                                            contrato__hotel__slug=self.slug)
            self._suplementos_dia = [ x for x in supl]
        return self._suplementos_dia

    def _get_precio(self, habitacion, info):
        contrato  = info.contrato
        #si se trata de una habitación base
        if (habitacion.tipo.is_individual  and  self.consulta.ocupacion == 1) or \
                      (self.consulta.ocupacion == 2):
            precio = info.precio_base
        else:
            try:
                supl = SuplementoOcupacion.objects.get(tipo_habitacion__parent__id=habitacion.tipo.id,
                                               tipo_habitacion__minimo=self.consulta.ocupacion,
                                               contrato__id = contrato.id,
                                               fecha_inicio__lte=info.fecha,
                                               fecha_fin__gte=info.fecha)
                precio = info.precio_base + supl.precio + info.precio_base*supl.porcentaje
            except SuplementoOcupacion.DoesNotExist:
                log.error('No existe precio para la habitacion %s en las fechas del contrato %s' \
                            % (habitacion.slug, contrato.id))
                log.error('Necesita introducir un suplemento ocupacion par %s paxes' % self.consulta.ocupacion)
                precio = None
        return precio


    def _suplementos_regimen(self):
        "Obtiene los suplementos de régimen asociados al hotel"
        tipos = self.disponiblidad.tipos
        hotel_id = self.model.pk
        suplementos = {}
        for tipo in tipos:
            total = 0
            for fecha in datetime_iterator(self.consulta.inicio, self.consulta.fin):
                try:
                    suplemento  = SuplementoRegimen.objects. \
                            get(hotel__id=hotel_id, regimen__pk= tipo, \
                            fecha_inicio__lt=fecha, fecha_fin__gt=fecha)
                    total += suplemento.precio
                except SuplementoRegimen.DoesNotExist:
                    total  = None
                    break
            if total:
                suplementos[tipo] = (total, suplemento.regimen)
        return suplementos


    def _establecer_precio_adultos(self, habitacion):
        """Establece el suplemento de ocupación de la habitación si
        lo hubiere. Retorna falso en caso de que no se pueda establecer,
        indicando que la habitación debe eliminarse del resultado"""

        for info in habitacion.inventario:
            precio = self._get_precio(habitacion, info)
            if not precio:
                return False
            else:
                info.precio_adultos=precio
        return True

    def _get_dto_ninyos(self, habitacion, info):
        """Establece el descuento de los niños"""
        try:
            dtos = DescuentoNin.objects.get(tipo_habitacion=habitacion.tipo.id,
                                            contrato__id = info.contrato.id,
                                            fecha_inicio__lte=info.fecha,
                                            fecha_fin__gte=info.fecha)
            dto = dtos.descuento(habitacion.consulta.ninyos)
        except DescuentoNin.DoesNotExist:
            log.error('No hay descuento de niños definido ni establecido. El contrato es erroneo')
            dto = None
        return dto

    def _establecer_dto_ninyos(self, habitacion):
        "Para cada día de la disponiblidad establece los descuentos"
        for info in habitacion.inventario:
            dto = self._get_dto_ninyos(habitacion, info)
            if not dto:
                return False
            else:
                info.add_dto_ninyos(dto)
        return True

    @property
    def contratos(self, refresh=False):
        if not self._contratos or refresh:
            contratos = []
            for k,x in self.habitaciones.items():
                contratos = contratos + x.contratos
            self._contratos = list(set(contratos))
        return self._contratos

    @property
    def habitaciones(self):
        if not self._cleaned:
            self._cleaned = True
            for k, habitacion in self._habitaciones.items():
                if not habitacion.is_valid():
                    self._habitaciones.pop(k)
                    log.debug('Habitacion %s eliminada' % habitacion)
                else:
                    if not self._establecer_precio_adultos(habitacion):
                        self._habitaciones.pop(k)
                    else:
                        if self.consulta.ninyos>0 and not self._establecer_dto_ninyos(habitacion):
                            log.error('Descuento de niños no establecido')
                            self._habitaciones.pop(k)
                            log.debug('Habitacion %s eliminada' % habitacion)
            # TODO a las ahbitaciones falta añadir los suplementos de régimen
        return self._habitaciones

    def is_valid(self):
        """Valida que el hotel tenga habitaciones y
        en caso afirmativo le asigna el suplemento de régimen"""
        valid = len(self.habitaciones)>0
        if valid:
            self.suplementos_regimen = self._suplementos_regimen()
        return valid


class Disponibilidad(object):
    """Una disponibiliad se refiere a un
    conjunto de hotels con sus respectivos tipos de habitaciones
    que pueden comprarse a partir de una seleccion"""

    def __init__(self, consulta):
        self._hoteles = {}
        self.consulta = consulta
        self._cleaned = False
        self.tipos = SuplementoRegimen.tipos()

    def add_hotel(self, dispo_hotel):
        """Añade un hotel a la lista de disponibles si no
        existía ya. Devuelve el hotel añadido"""
        if not dispo_hotel.slug in self._hoteles:
            hotel = Hotel(dispo_hotel, self)
            self._hoteles[dispo_hotel.slug] = hotel
        return  self._hoteles[dispo_hotel.slug]

    @property
    def hoteles(self):
        """Devuelve una lista de hoteles que cumplen
        con los criteros de disponiblidad"""

        if not self._cleaned:
            for k, hotel in self._hoteles.items():
                if not hotel.is_valid():
                    self._hoteles.pop(k)
            self._cleaned=True
        return self._hoteles

    def __str__(self):
        if not self.hoteles.items():
            return  "No hay disponibilidad"
        rta =""
        for k, hotel in self.hoteles.items():
            rta = rta+"%s %s" % ( hotel.slug, hotel.model.nombre)
            for k, habitacion in hotel.habitaciones.items():
                rta = rta + "\t%s %s %s" % (habitacion.slug, habitacion.tipo, habitacion.regimen)
                for dia in habitacion.inventario:
                    rta = rta+  "\t\t%s%s%s%s" %( dia.fecha, dia.precio_base, dia.cupo, dia.is_apartamento, )
        return rta

    def obtener_disponibilidad(self):
        consulta = self.consulta
        disponibilidad = Inventario.objects.filter(fecha__gte=consulta.inicio,
                                               fecha__lte=consulta.fin,
                                               cupo_actual__gte=consulta.num_habitaciones,
                                               is_paro_ventas = False)
        if consulta.tipo_habitacion:
            disponibilidad = disponibilidad.filter(tipo_habitacion__id = consulta.tipo_habitacion)
        # Si hay un hotel filtramos por ese hotel
        if consulta.hotel:
            disponibilidad = disponibilidad.filter(hotel__id=consulta.hotel.id)
        disponibilidad = disponibilidad.order_by('hotel', 'tipo_habitacion', 'regimen', 'fecha')
        for dispo in disponibilidad:
            hotel = self.add_hotel(dispo.hotel)
            habitacion = hotel.add_habitacion(Habitacion(dispo.tipo_habitacion, dispo.regimen, hotel))
            info = Info(dispo.fecha, dispo.cupo_actual, dispo.precio,
                        dispo.is_apartamento, dispo.contrato)
            habitacion.add_inventario(info)
