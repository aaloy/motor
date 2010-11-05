#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Vistas para el testeo de disponibilidad
"""

from motor.core.tarificador import Disponibilidad
from django.views.generic.simple import direct_to_template
from motor.core.consulta import Consulta
from datetime import date, timedelta
from forms import BuscarForm
LIMITE_BEBES = 2 # se consideran bebés los niños menores de 2 años

def disponibilidad_2ad(request):
    """Ejemplo de disponibilidad para dos adultos"""
    consulta = Consulta(date.today()+timedelta(days=5),
                            noches=5,
                            adultos = 2,
                            ninyos = 0,
                           )
    dispo = Disponibilidad(consulta)
    dispo.obtener_disponibilidad()
    form = BuscarForm()
    return direct_to_template(request, template='recepcion/disponibilidad.html',
                              extra_context={'dispo': dispo, 'consulta':consulta,
                                             'form':form})

def disponibilidad_2ad_1n(request):
    """Ejemplo de disponibilidad de dos adultos y un niño"""
    consulta = Consulta(date.today()+timedelta(days=5),
                            noches=5,
                            adultos = 2,
                            ninyos = 1,
                           )
    dispo = Disponibilidad(consulta)
    dispo.obtener_disponibilidad()
    form = BuscarForm()
    return direct_to_template(request, template='recepcion/disponibilidad.html',
                              extra_context={'dispo': dispo, 'consulta':consulta, 'form':form})


def disponibilidad(request):
    """Buscador de disponibilidad"""
    data = {}
    if request.method == "POST":
        form = BuscarForm(request.POST)
        if form.is_valid():
            # procesamos la dispo
            hotel = form.cleaned_data['hotel']
            noches = form.cleaned_data['fecha_salida'] - form.cleaned_data['fecha_llegada']
            # Eliminamos los bebés de la dispo
            nins = 0
            for x in range(1, form.cleaned_data['nins_d1']+1):
                if form.cleaned_data['edad_nin%s_d1' % x ]>2:
                    nins += 1
            consulta = Consulta(
               inicio = form.cleaned_data['fecha_llegada'],
               noches = noches.days,
               adultos = form.cleaned_data['adultos_d1'],
               ninyos = nins,
               hotel = hotel
            )
            dispo = Disponibilidad(consulta)
            dispo.obtener_disponibilidad()
            data['consulta'] = consulta
            data['dispo'] = dispo
    else:
        form = BuscarForm()
    data['form'] = form
    return direct_to_template(request, template='recepcion/disponibilidad.html', extra_context=data)
