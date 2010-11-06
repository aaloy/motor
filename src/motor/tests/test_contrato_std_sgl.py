#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from motor.models import Hotel, Contrato, CondicionesContrato, Inventario
from motor.models import Regimen, TipoHabitacion, RestriccionOcupacion
from motor.core.consulta import Consulta
from motor.core.tarificador import Disponibilidad
from datetime import date, timedelta
from nose import tools
import logging
log = logging.getLogger(__name__)

class ContratoStdSglTestcase(TestCase):
    """"Comprobación de definición de contratos
        La definición del contrto corresponde al hotel-pepito.odt
        Comprobamos la disponibilidad para single en su modalidad
        de doble uso y habitaición individual
    """
    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_std.json']


    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()

    def tearDown(self):
        pass

    def test_precio_single(self):
        """Comprueba que tenemos precios correctos para la habitación
        en el caso de la consulta individual"""
        # 2 AD 1 día
        log.debug('Test precio single')
        consulta = Consulta(date.today()+timedelta(days=2),
                            1,
                            adultos = 1
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==2 #tiene que estar la std y ls ind 
        assert hotel.habitaciones.get('ind-mp').precio == 60, "El precio no concuerda %s" %  hotel.habitaciones.get('ind-mp').precio
        assert hotel.habitaciones.get('std-mp').precio == 60, "El precio no concuerda %s" % hotel.habitaciones.get('std-mp').precio


    def test_precio_single_noches(self):
        """Comprueba que tenemos precios correctos para la habitación
        en el caso de la consulta individual para más de una noche"""
        # 2 AD 1 día
        log.debug('Test precio single')
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=4,
                            adultos = 1
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==2 #tiene que estar la std y ls ind 
        assert hotel.habitaciones.get('ind-mp').precio == 240, "El precio no concuerda %s" %  hotel.habitaciones.get('ind-mp').precio
        assert hotel.habitaciones.get('std-mp').precio == 240, "El precio no concuerda %s" % hotel.habitaciones.get('std-mp').precio

    def test_no_suite(self):
        """Comprueba que no hay disponiblidad si selecccionamos una suite"""
        log.debug('Test precio single para Suite')
        consulta = Consulta(date.today()+timedelta(days=2),
                            tipo_habitacion = 3,
                            noches=4,
                            adultos = 1
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==0, "No debería haber disponibilidad"
 
