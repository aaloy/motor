#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django import forms
from motor.models import Hotel

class BuscarForm(forms.Form):
    """Buscador de disponibilidad"""
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all().order_by('nombre'),
                                   empty_label="(Todos los hoteles)")


