#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from motor.models import Contrato, RestriccionOcupacion
from motor.core.consulta import Consulta
from motor.core.tarificador import Disponibilidad
from datetime import date, timedelta
import nose

class RestriccionTestcase(TestCase):
    """
    Comprueba que la restricción de ocupación funciona
    """

    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_res_ocupacion.json']

    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()

    def tearDown(self):
        pass

    def test_restriccion_ocupacion_ninyos(self):
        """Comprueba que la restricción de ocupación se aplica.
        Se está consultando la ocupación de 2 adultos y dos niños
        """
        assert RestriccionOcupacion.objects.all().count() > 0, "No hay restricciones de ocupación en el contrato"
        consulta = Consulta(date.today()+timedelta(days=2) , 
                            tipo_habitacion=2,
                            noches=4, ninyos=1)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 0 , "No Debe haber un hotel"

    def test_restriccion_ocupacion_adultos(self):
        """Comprueba que la restricción de ocupación se aplica.
        Se está consultando la ocupación de 2 adultos y dos niños
        """
        assert RestriccionOcupacion.objects.all().count() > 0, "No hay restricciones de ocupación en el contrato"
        consulta = Consulta(date.today()+timedelta(days=2) , 
                            tipo_habitacion=2,
                            noches=4, ninyos=0,
                            adultos=1)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 0 , "No Debe haber un hotel"


