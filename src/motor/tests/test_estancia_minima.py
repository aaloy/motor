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

class EstanciaMinimaTestcase(TestCase):
    """
    """
    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_std_estancia.json']


    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()

    def tearDown(self):
        pass

    def test_estancia_minima(self):
        """"Comprobamos que no se puede reservar con una
        estancia mínima menor que la fijada en contrato"""

        log.info('Comprobamos primero que sin la restriccion tenemos dispo')
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=5,
                            adultos = 2,
                            ninyos = 0,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "Debería salir un hotel"

        log.info('Ahora con la restricción')
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=2,
                            adultos = 2,
                            ninyos = 0,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==0, "No debería haber hotel"


