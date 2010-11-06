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

class ContratoStdTestcase(TestCase):
    """"Comprobación de definición de contratos
        La definición del contrto corresponde al hotel-pepito.odt
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

    def test_check_carga(self):
        "Comprueba que hemos podido cargar los datos"
        assert Hotel.objects.all().count() > 0, "No se han cargado los hoteles"
        assert Regimen.objects.all().count() > 0, "No se ha cargado el régimen"
        assert TipoHabitacion.objects.all().count() > 0
        assert  CondicionesContrato.objects.all().count() >0, "No se han cargado las condiciones"
        assert  Inventario.objects.filter(contrato__id=1, tipo_habitacion__id=1).count() > 0, \
                "No se ha generado el inventario para el tipo de habitación 1"
        assert  Inventario.objects.filter(contrato__id=1, tipo_habitacion__id=2).count() >0, \
                "No se ha generado el inventario para el tipo de habitación 2"

    def test_disponibilidad_basica(self):
        """Comprueba una disponiblidad básica 2 ad 4 noches"""
        consulta = Consulta(date.today()+timedelta(days=2) ,
                            noches = 4,
                            adultos = 2)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1 , "Debe haber un hotel"
        hotel = dispo.hoteles['test']
        assert  len(hotel.habitaciones) == 2

    def test_sin_dispo(self):
        """Comprueba que no devuelve disponibilidad si las condiciones
        de ocupación no se cumplen"""
        consulta = Consulta(date.today()+timedelta(days=2) ,
                            4,
                            adultos=4, ninyos=2)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 0 , "No Debe haber un hotel"

    def test_dispo_suite(self):
        """Comprueba que hay disponiblidad para la suite"""
        consulta = Consulta(date.today()+timedelta(days=2),
                            4,
                            tipo_habitacion = 3
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1 , "Debe haber un hotel"
        hotel = dispo.hoteles['test']
        assert  len(hotel.habitaciones) == 1

    def test_precio_doble_std(self):
        """Comprueba que tenemos precios correctos para la habitación
        en el caso de la habitación std"""
        # 2 AD 1 día
        consulta = Consulta(date.today()+timedelta(days=2),
                            1,
                            tipo_habitacion = 2, #std
                            adultos = 2
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==1, "No hay habitaciones"
        habitacion = hotel.habitaciones.get('std-mp')
        assert habitacion.precio == 100, "El precio no concuerda (%s)" % habitacion.precio
        # 2 adultos
        consulta = Consulta(date.today()+timedelta(days=2),
                            4,
                            tipo_habitacion = 2, #std
                            adultos = 2
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==1, "No hay habitaciones"
        habitacion = hotel.habitaciones.get('std-mp')
        assert habitacion.precio == 400, "El precio no concuerda (%s)" % habitacion.precio
        # 3 adultos
        consulta = Consulta(date.today()+timedelta(days=2),
                            4,
                            tipo_habitacion = 2, #std
                            adultos = 3
                           )
        #1 adulto
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==1, "No hay habitaciones"
        habitacion = hotel.habitaciones.get('std-mp')
        assert habitacion.precio == 480, "El precio no concuerda"
        consulta = Consulta(date.today()+timedelta(days=2),
                            4,
                            tipo_habitacion = 2, #std
                            adultos = 1
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert len(hotel.habitaciones)==1, "No hay habitaciones"
        habitacion = hotel.habitaciones.get('std-mp')
        assert habitacion.precio == 240, "El precio no concuerda"

