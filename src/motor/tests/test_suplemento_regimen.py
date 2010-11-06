#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from motor.models import Hotel, Contrato, CondicionesContrato, Inventario
from motor.models import Regimen, TipoHabitacion, RestriccionOcupacion, SuplementoRegimen

from motor.core.consulta import Consulta
from motor.core.tarificador import Disponibilidad
from datetime import date, timedelta
from nose import tools
import logging
log = logging.getLogger(__name__)
from decimal import Decimal

class SuplementoRegimenTestcase(TestCase):
    """"Comprobación de definición de contratos
        La definición del contrto corresponde al hotel-pepito.odt
        Comprobamos la disponibilidad para single en su modalidad
        de doble uso y habitaición individual

        Comprobamos que funciona el descuento de niños

    """
    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_std.json',
                'suplementos_regimen.json']


    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()

    def tearDown(self):
        pass

    def test_hay_suplementos(self):
        """Comprueba que hay suplementos de régimen definidos"""
        supl = SuplementoRegimen.objects.all().count() > 0

    def test_check_tipos(self):
        """Comprueba que obtenemos los tipos"""
        assert 2 in SuplementoRegimen.tipos(), "Falta el tipo de regimen 2"
        assert 3 in SuplementoRegimen.tipos(), "Falta el tipo de regimen 3"

    def test_get_precios(self):
        consulta = Consulta(date.today()+timedelta(days=2) , noches=4)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1 , "Debe haber un hotel"
        hotel = dispo.hoteles['test']
        assert len(hotel.suplementos_regimen) > 0, "No hay suplementos de regimen"
