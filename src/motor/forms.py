#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Formularios para el mantenimiento de los contratos.
"""

from motor.models import Contrato
from motor.models import CondicionesContrato
from motor.models import DescuentoNin
from motor.models import SuplementoRegimen
from motor.models import SuplementoOcupacion
from motor.models import SuplementoDia
from motor.models import RestriccionEstanciaMinima
from motor.models import RestriccionOcupacion
from motor.models import RestriccionBlackout

from django.forms import ModelForm

class ContratoForm(ModelForm):
    class Meta:
        model = Contrato


class CondicionesContratoForm(ModelForm):
    class Meta:
        model = CondicionesContrato
        exclude = ('contrato',)

class DescuentoNinyosForm(ModelForm):
    class Meta:
        model = DescuentoNin
        exclude = ('contrato',)

class SuplementoRegimenForm(ModelForm):
    class Meta:
        model = SuplementoRegimen
        exclude = ('hotel', )

class SuplementoOcupacionForm(ModelForm):
    class Meta:
        model = SuplementoOcupacion
        exclude = ('contrato',)


class SuplementoDiaForm(ModelForm):
    class Meta:
        model = SuplementoDia
        exclude = ('contrato',)

class RestriccionEstanciaMinimaForm(ModelForm):
    class Meta:
        model = RestriccionEstanciaMinima
        exclude = ('contrato',)


class RestriccionOcupacionForm(ModelForm):
    class Meta:
        model = RestriccionOcupacion
        exclude = ('contrato',)

class RestriccionBlackoutForm(ModelForm):
    class Meta:
        model = RestriccionBlackout
        exclude = ('contrato', )
