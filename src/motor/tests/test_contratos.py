#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.test import TestCase
from motor.models import Hotel, Contrato, CondicionesContrato, Inventario
from motor.models import Regimen, TipoHabitacion, RestriccionOcupacion
from motor.core.consulta import Consulta
from motor.core.tarificador import Disponibilidad
from datetime import date, timedelta
import nose
import logging
log = logging.getLogger(__name__)

class ContratosTestcase(TestCase):
    """"Comprobación de definición de contratos

    El fitxure define el siguiente contrato:

        Hotel con 2 tipos de habitaciones:
            std: habitación estándard en régimen de media pensión
                ocupación mínima 1 adulto, máximo 3 niños. Máximo por habitación 5
            sui: habitación suite en régimen de media pension.
                ocupació mínima 2 adultos, máximo 3 niños. Máximo por habitación 6

        Contrato
        --------
        ver contrato std_todo

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

    def test_hoteles_definidos(self):
        "Comprueba que hemos podido cargar los hoteles"
        assert Hotel.objects.all().count() > 0, "No se han cargado los hoteles"


    def test_carga_regimen(self):
        "Comprueba la carga del regimen de pruebas"
        assert Regimen.objects.all().count() > 0, "No se ha cargado el régimen"

    def test_tipo_habitacion(self):
        "Comprueba que se ha cargado el tipo de habitacion"
        assert TipoHabitacion.objects.all().count() > 0

    def test_contratos_definidos(self):
        "Compueba que se han cargado las condiciones"
        assert  CondicionesContrato.objects.all().count() >0, "No se han cargado las condiciones"

    def test_carga_inventario(self):
        "Comprueba que se genera el inventario"
        assert  Inventario.objects.filter(contrato__id=1, tipo_habitacion__id=1).count() > 0, \
                "No se ha generado el inventario para el tipo de habitación 1"
        assert  Inventario.objects.filter(contrato__id=1, tipo_habitacion__id=2).count() >0, \
                "No se ha generado el inventario para el tipo de habitación 2"

    def test_disponibilidad_basica(self):
        """Comprueba una disponiblidad básica 2 ad 4 noches"""
        consulta = Consulta(date.today()+timedelta(days=2) , noches=4)
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1 , "Debe haber un hotel"
        hotel = dispo.hoteles['test']
        assert len(hotel.contratos) == 1, "Hay un contrato"
        assert  len(hotel.habitaciones) == 2

    def test_paro_ventas(self):
        """Comprobamos que si entre el rango de fechas hay un paro de ventas para
        esa habitación no sale"""
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=4)
        fecha = date.today()+timedelta(days=4)
        for inv in Inventario.objects.filter(fecha=fecha, tipo_habitacion__slug='sui'):
            inv.is_paro_ventas = True
            inv.save()
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        assert len(dispo.hoteles) == 1 , "Debe haber un hotel"
        hotel = dispo.hoteles['test']
        assert len(hotel.habitaciones) == 1

    def test_dispo_str(self):
        "Comprueba que existe representación textual para la dispo"
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=4)
        fecha = date.today()+timedelta(days=4)
        for inv in Inventario.objects.filter(fecha=fecha, tipo_habitacion__slug='sui'):
            inv.is_paro_ventas = True
            inv.save()
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        log.info(dispo)
        assert len("%s" % dispo) > 0, "Debería haber disponiblidad"

    def test_sin_dispo_str(self):
        "Comprueba que existe representación textual para la dispo"
        consulta = Consulta(date.today()+timedelta(days=2),
                            noches=3, adultos=10)
        fecha = date.today()+timedelta(days=4)
        for inv in Inventario.objects.filter(fecha=fecha, tipo_habitacion__slug='sui'):
            inv.is_paro_ventas = True
            inv.save()
        dispo = Disponibilidad(consulta)
        dispo.obtener_disponibilidad()
        log.info(dispo)
        assert "%s"%dispo == "No hay disponibilidad"

