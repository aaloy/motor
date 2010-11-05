#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Urls para la aplicación de RECEPCION."""

from django.conf.urls.defaults import patterns, url
from motor.models import Hotel

urlpatterns = patterns('',
    url(r'^listado-hoteles/$', 'django.views.generic.list_detail.object_list',
        {'queryset': Hotel.objects.all(),
         'template_name': 'recepcion/hoteles.html'},
        name='listado-hoteles'),
    url(r'^listado-contratos/$','django.views.generic.list_detail.object_list',
        {'queryset': Hotel.objects.all(),
         'template_name': 'recepcion/hotel_list.html'},
            name="listado-contratos"),
    url(r'contrato-hotel/(?P<slug>[\w_-]+)/$', 'django.views.generic.list_detail.object_detail',
        {'queryset': Hotel.objects.all(),
         'template_name': 'recepcion/contrato_hotel.html',
         'slug_field': 'slug'},
        name="contrato-hotel"),
    url(r'^disponibilidad2ad/$', 'recepcion.views.disponibilidad_2ad', name="disponibilidad-2ad"),
    url(r'^disponibilidad2ad1n/$', 'recepcion.views.disponibilidad_2ad_1n', name="disponibilidad-2ad-1n"),
    url(r'^disponibilidad/$', 'recepcion.views.disponibilidad', name="disponibilidad"),
    )
