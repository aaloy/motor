#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Test de tipos básicos
"""

from django.test import TestCase
from motor.models import Regimen
from motor.models import TipoHabitacion
import nose

class RegimenTestcase(TestCase):
    "Comprobación de régimen"

    fixtures = ['regimen.json',]

    def test_regimenes_definidos(self):
        "Comprueba que hemos definido un regimen"
        assert Regimen.objects.all().count() > 0, "Esta vacío"

class TipoHabitacionTestcase(TestCase):
    "Comprobación de tipo de habitacion"

    fixtures = ['tipohabitacion.json', ]

    def test_tipos_definidos(self):
        "Comprueba que hemos cargado los tipos de habitacion"
        assert TipoHabitacion.objects.all().count() > 0
        assert TipoHabitacion.objects.all().count() == 8, "Tendría que haber 8 habitaciones definidas"

    def test_valid(self):
        """"Comprueba is_valid."""
        habitacion  =TipoHabitacion.objects.get(slug='std')

        nose.tools.assert_false(
            habitacion.is_valid(adultos=3, ninyos=2),
            "Se ha superado el máximo")

        nose.tools.assert_true(
            habitacion.is_valid(adultos = 2, ninyos = 2),
            "No es mayor que el máximo total (4)")

        nose.tools.assert_false(
            habitacion.is_valid(adultos=4, ninyos= 2),
            "No se permite más que un total de 4 por habitación")

        nose.tools.assert_false(
            habitacion.is_valid(adultos=1, ninyos=3),
                "Supera el límite de niños")

        nose.tools.assert_false(
            habitacion.is_valid(adultos=6, ninyos=0),
                "Superado el máximo de adultos")

        nose.tools.assert_false(
            habitacion.is_valid(adultos=0, ninyos=0),
                "No se permiten cero adultos y cero niños")

        nose.tools.assert_false(
            habitacion.is_valid(adultos=0, ninyos=1),
                "No se permiten habitaciones sin niños")


