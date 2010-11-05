#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django import forms
from motor.models import Hotel
from captcha.fields import CaptchaField

"""Definición de los formularios del front-end"""
MAX_ROOMS = 1 # por ahora el motor no admite distribución
MAX_ADULTS = 4
MAX_NINS = 3
MAX_AGE = 12

class BuscarForm(forms.Form):
    """Formulario de búsqueda"""
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all().order_by('nombre') , empty_label="(Todos)", required=False)
    fecha_llegada = forms.DateField(help_text="Fecha de entrada al hotel", input_formats=('%d/%m/%Y',))
    fecha_salida  = forms.DateField(help_text="Fecha de salida del hotel", input_formats=('%d/%m/%Y',))
    habitaciones = forms.TypedChoiceField(choices=[(x,x) for x in range(1,MAX_ROOMS+1)] ,coerce=int)
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super(BuscarForm, self).__init__(*args, **kwargs)
        for i in range(1, MAX_ROOMS+1):
            self.fields['adultos_d%s' % i] = forms.TypedChoiceField(choices = [(x,x) for x in range(1, MAX_ADULTS+1)], coerce=int)
            self.fields['nins_d%s' %i] = forms.TypedChoiceField(choices = [(x,x) for x in range(0, MAX_NINS+1)],
                                                                coerce =int,
                                                                widget = forms.Select( attrs={'class':'nins'} ))
            for j in range(1, MAX_NINS+1):
                self.fields['edad_nin%s_d%s' % (j, i)] = forms.TypedChoiceField(choices = [(x,x) for x in range(0, MAX_AGE+1)], coerce=int)


