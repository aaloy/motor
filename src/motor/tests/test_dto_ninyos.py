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
from decimal import Decimal

class ContratoStdDtoNinyosTestcase(TestCase):
    """"Comprobación de definición de contratos
        La definición del contrto corresponde al hotel-pepito.odt
        Comprobamos la disponibilidad para single en su modalidad
        de doble uso y habitaición individual

        Comprobamos que funciona el descuento de niños

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

    def test_precio_1N_2AD_1N(self):
        """Comprueba que tenemos precios correctos para la habitación
        en el caso de la consulta individual"""
        # 2 AD 1 día
        consulta = Consulta(date.today()+timedelta(days=2),
                            1,
                            tipo_habitacion=2,
                            adultos = 2,
                            ninyos = 1,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert hotel.habitaciones.get('std-mp').precio == 88

    def test_precio_1N_1AD_1N(self):
        "Un adulto y un niño. Implica habitación doble"
        consulta = Consulta(date.today()+timedelta(days=2),
                            1,
                            tipo_habitacion = 2,
                            adultos = 1,
                            ninyos = 1,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert hotel.habitaciones.get('std-mp').precio == Decimal("60")


    def test_precio_1N_2AD_2N(self):
        "Dos adultos y dos niños"
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=1,
                            tipo_habitacion = 2,
                            adultos = 2,
                            ninyos = 2,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "No hay disponibilidad"
        hotel = dispo.hoteles.get('test')
        assert hotel.habitaciones.get('std-mp').precio ==  Decimal("87.5"), \
                "Da %s"% hotel.habitaciones.get('std-mp').precio


    def test_precio_1N_1AD_3N(self):
        """Un adulto y tres niños. No hay disponiblidad, ya
        que están las habitaciones a un máximo de 2 niños"""
        consulta = Consulta(date.today()+timedelta(days=2),
                            1,
                            tipo_habitacion = 2,
                            adultos = 1,
                            ninyos = 3,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==0, "No debiera haber disponibilidad"

