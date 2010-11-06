#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from motor.models import Hotel, Contrato, CondicionesContrato, Inventario
from motor.models import Regimen, TipoHabitacion, RestriccionOcupacion
from motor.models import SuplementoDia
from motor.core.consulta import Consulta
from motor.core.tarificador import Disponibilidad
from datetime import date, timedelta
from nose import tools
import logging
log = logging.getLogger(__name__)
from decimal import Decimal

class SuplementoDiaTestcase(TestCase):
    """
    """
    fixtures = ['hoteles.json',
                'regimen.json',
                'tipohabitacion.json',
                'contrato_std_suplemento_dia.json']


    def setUp(self):
        contrato = Contrato.objects.get(pk=1)
        contrato.revisado = True
        contrato.activo = True
        contrato.save()
        # Suplemento cena gala adultos
        dia = date.today()+timedelta(days=5)
        supl = SuplementoDia(contrato = contrato,
                             fecha = dia,
                             descripcion="Cena de gala",
                             precio = Decimal("50"),
                             porcentaje=Decimal("0"),
                             aplicabilidad='A')
        supl.save()

    def tearDown(self):
        pass

    def test_suplemento_dia(self):
        "Comprobamos que se aplican los suplementos"
        consulta = Consulta(date.today()+timedelta(days=3),
                            noches=4,
                            adultos = 2,
                            ninyos = 0,
                           )
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles)==1, "Debería salir un hotel"
        hotel = dispo.hoteles.get('test')
        habitacion = hotel.habitaciones.get('std-mp')
        assert habitacion.precio == 500


