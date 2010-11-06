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

class BlackoutTestcase(TestCase):
    """
    """
    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_std_blackout.json']


    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()

    def tearDown(self):
        pass

    def test_blackout(self):
        """"Comprobamos que no se puede reservar con una
        antelación menor que el blackout"""
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=1,
                            adultos = 2,
                            ninyos = 2,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==0, "Hay blackout de 3 días y no debe haber dispo"

