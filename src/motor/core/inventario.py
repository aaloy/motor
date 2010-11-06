#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Reglas de negocio para el inventario
"""
from django.db import transaction
from motor.core.interval import datetime_iterator
from datetime import timedelta

import logging
log = logging.getLogger(__name__)

@transaction.commit_on_success
def crear_inventario(contrato):
    """Crea el inventario para un contrato"""
    from motor.models import Inventario
    for condicion in contrato.condicionescontrato_set.filter(is_cupo_generado=False):
        for fecha in datetime_iterator(condicion.fecha_inicio, condicion.fecha_fin):
            inventario = Inventario()
            inventario.fecha = fecha
            inventario.contrato = contrato
            inventario.hotel = contrato.hotel
            inventario.regimen = condicion.regimen
            inventario.tipo_habitacion = condicion.tipo_habitacion
            inventario.cupo_inicial = condicion.cupo
            inventario.cupo_actual = condicion.cupo
            inventario.precio = condicion.precio
            inventario.is_apartamento = condicion.is_apartamento
            inventario.is_paro_ventas = condicion.is_paro_ventas
            inventario.is_venta_libre = condicion.is_venta_libre
            inventario.save()
            #log.debug('Generado inventario para %s del contrato %s' % (fecha, contrato))
        condicion.is_cupo_generado = True
        condicion.save()
        log.info('Generado inventario del contrato %s desde %s a %s' % (contrato, condicion.fecha_inicio, condicion.fecha_fin))
        log.debug('Hay %s lineas de inventario ' %  Inventario.objects.all().count())

@transaction.commit_on_success
def crear_inventario_condicion(condicion):
    """Añade el inventario para una condición.
    Precondiciones: El contrato está revisado y es activo
    y la condición no ha sido ya inventariada"""

    from motor.models import Inventario
    contrato = condicion.contrato
    if contrato.activo and contrato.revisado and  not condicion.is_cupo_generado:
        for fecha in datetime_iterator(condicion.fecha_inicio, condicion.fecha_fin):
            inventario = Inventario()
            inventario.fecha = fecha
            inventario.contrato = contrato
            inventario.hotel = contrato.hotel
            inventario.regimen = condicion.regimen
            inventario.tipo_habitacion = condicion.tipo_habitacion
            inventario.cupo_inicial = condicion.cupo
            inventario.cupo_actual = condicion.cupo
            inventario.precio = condicion.precio
            inventario.is_apartamento = condicion.is_apartamento
            inventario.is_paro_ventas = condicion.is_paro_ventas
            inventario.is_venta_libre = condicion.is_venta_libre
            inventario.save()
        condicion.is_cupo_generado = True
        condicion.save()
        log.debug('Generado inventario desde %s a %s del contrato %s' % (condicion.fecha_inicio,
                                                                         condicion.fecha_fin,
                                                                         contrato))


class ReservaQuery(object):
    """Define los datos necesarios para realizar una disponiblidad
    en el motor"""

    def __init__(self, adultos, entrada, noches, habitaciones=1, children=0):
        self.adultos = adultos
        self.entrada = entrada
        self.noches = noches
        self.habitaciones = habitaciones
        self.children = children
        self.regimen = None
        self.tipo_habitacion = None
        self.hotel = None
        self.edades = []

    def set_regimen(self, value):
        """Indica que se quiere buscar por un régimen predefinido"""
        self.regimen = value

    def set_tipo_habitacion(self, value):
        """Indica que se quiere buscar por un tipo de habitación predefinida"""
        self.tipo_habitacion = value

    def set_hotel(self, value):
        """Indica que queremos buscar por un hotel en concreto"""
        self.hotel = value

    def set_edades(self, value):
        self.edades = value

    @property
    def salida(self):
        return self.entrada +  timedelta(days = self.noches)

    @property
    def dias_tarificacion(self):
        return self.entrada, self.entrada+timedelta(days = self.noches -1) 
