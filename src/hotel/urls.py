#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Urls para la aplicación del front end de hotel."""

from django.conf.urls.defaults import patterns, url
from motor.models import Hotel

urlpatterns = patterns('hotel.views',
    url(r'^recepcion/$', 'disponibilidad', name="recepcion"),
    url(r'^disponibilidad/$', 'disponibilidad', name="disponibilidad"),
    )
