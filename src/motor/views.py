#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template, redirect_to
from jsonrpc import jsonrpc_method

from forms import ContratoForm, CondicionesContratoForm, DescuentoNinyosForm, SuplementoRegimenForm, SuplementoOcupacionForm, SuplementoDiaForm, RestriccionEstanciaMinimaForm, RestriccionOcupacionForm, RestriccionBlackoutForm
from models import Hotel, Contrato, CondicionesContrato, DescuentoNin, SuplementoRegimen, SuplementoOcupacion, SuplementoDia, RestriccionEstanciaMinima, RestriccionOcupacion, RestriccionBlackout

@jsonrpc_method('contratos(String)', safe=True)
def contratos(request):
    rta = Contrato.objects.all().values('id')
    return list(rta)

def nuevo_contrato(request, id=None):
    """Modificación y alta de la cabecera de un contrato"""
    form = ContratoForm(request.POST or None,
                        instance = id and Contrato.objects.get(id=id))
    if request.method == 'POST':
        if form.is_valid():
            contrato = form.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                                             args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/nuevo_contrato.html',
                              extra_context = {'form':form})


def editar_condiciones(request, contrato_id, id=None):
    """Modificación y alta de la cabecera de un contrato"""
    name ="Condiciones del Contrato"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = CondicionesContratoForm(request.POST or None,
                        instance = id and CondicionesContrato.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                                     args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name})

def editar_descuento_ninyos(request, contrato_id, id=None):
    """Descuento niños"""
    name="Descuento Niños"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = DescuentoNinyosForm(request.POST or None,
                        instance = id and DescuentoNin.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                                     args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name})

def editar_suplemento_regimen(request, hotel_id, id=None):
    """Los suplementos de regimen van por hotel"""
    name = "Suplementos de Régimen"
    hotel = Hotel.objects.get(pk=hotel_id)
    form = SuplementoRegimenForm(request.POST or None,
                        instance = id and SuplementoRegimen.objects.get(id=id, hotel__id = hotel_id))
    if request.method == 'POST':
        form.instance.hotel = hotel
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.hotel = hotel
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                                     args = [hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'name':name })

def editar_suplemento_ocupacion(request, contrato_id, id=None):
    """Los suplementos de ocupacion"""
    name ="Suplementos de Ocupacion"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = SuplementoOcupacionForm(request.POST or None,
                        instance = id and SuplementoOcupacion.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                                     args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name })


def editar_suplemento_dia(request, contrato_id, id=None):
    """Los suplementos por día"""
    name = "Suplementos por día"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = SuplementoDiaForm(request.POST or None,
                        instance = id and SuplementoDia.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                         url = reverse('contrato-hotel',
                         args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name })

def editar_restriccion_estancia_minima(request, contrato_id, id=None):
    """Restriccion de estancia mínima"""
    name ="Restricción de estancia mínima"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = RestriccionEstanciaMinimaForm(request.POST or None,
                        instance = id and RestriccionEstanciaMinima.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                               args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name })

def editar_restriccion_ocupacion(request, contrato_id, id=None):
    """Restriccion de ocupacion"""
    name ="Restricción de Ocupación"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = RestriccionOcupacionForm(request.POST or None,
                        instance = id and RestriccionOcupacion.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                            url = reverse('contrato-hotel',
                            args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name })

def editar_restriccion_blackout(request, contrato_id, id=None):
    """Restriccion de blackout"""
    name = "Restricción de Blackout"
    contrato = Contrato.objects.get(pk=contrato_id)
    form = RestriccionBlackoutForm(request.POST or None,
                        instance = id and RestriccionBlackout.objects.get(id=id, contrato__id = contrato_id))
    if request.method == 'POST':
        form.instance.contrato = contrato
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.contrato = contrato
            condicion.save()
            return redirect_to(request,
                               url = reverse('contrato-hotel',
                               args = [contrato.hotel.slug,]))
    return direct_to_template(request,
                              template = 'motor/condiciones_contrato.html',
                              extra_context = {'form':form, 'contrato':contrato, 'name':name })


