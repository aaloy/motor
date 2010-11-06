#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from motor.models import Hotel
from django.template.loader import render_to_string


""""Utilidades para la gestión de contratos"""

def get_contratos(hotel_id, plantilla='contrato.html'):
    """Dado un hotel imprime la información que tenemos relativa a sus contratos"""
    hotel = Hotel.objects.get(pk=hotel_id)
    texto = u"%s" % render_to_string(plantilla, {'hotel':hotel})
    return texto
