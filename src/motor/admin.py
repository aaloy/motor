#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.contrib import admin
from models import TipoHabitacion
from models import Regimen
from models import Hotel
from models import Contrato
from models import CondicionesContrato
from models import Inventario
from models import SuplementoRegimen
from models import SuplementoOcupacion
from models import SuplementoDia
from models import DescuentoNin
from models import RestriccionOcupacion
from models import RestriccionEstanciaMinima
from models import RestriccionBlackout


class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'descripcion', 'minimo', 'maximo', 'children', 'is_base', 'is_individual', 'parent')
    list_filter = ('parent', 'is_base', 'is_individual')

class RegimenAdmin(admin.ModelAdmin):
    list_display = ('slug','descripcion', 'is_base', 'parent')
    list_filter = ('parent', 'is_base')


class ContratoInline(admin.TabularInline):
    model = Contrato
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nombre')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ContratoInline, ]

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hotel', 'fecha_inicio', 'fecha_fin', 'activo', 'revisado')
    list_filter = ('hotel', 'activo', 'revisado')

class CondicionesContratoAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'regimen', 'tipo_habitacion', 'cupo', 'precio')
    list_filter = ('contrato', 'regimen', 'tipo_habitacion')

class InventarioAdmin(admin.ModelAdmin):
    list_display =  ('contrato', 'hotel', 'fecha', 'regimen', 'tipo_habitacion', 'cupo_inicial','cupo_actual', 'precio',
                    'is_apartamento', 'is_paro_ventas', 'is_venta_libre')
    list_filter = ('contrato', 'hotel', 'fecha','regimen', 'tipo_habitacion', 'is_paro_ventas')

class SuplementoRegimenAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'fecha_inicio', 'fecha_fin', 'regimen',  'precio', )
    list_filter = ('hotel', 'regimen', 'fecha_inicio', 'fecha_fin')

class SuplementoOcupacionAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'tipo_habitacion',  'precio', 'porcentaje')
    list_filter = ('contrato', 'tipo_habitacion', 'fecha_inicio', 'fecha_fin')

class SuplementoDiaAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'fecha', 'descripcion', 'aplicabilidad', 'precio', 'porcentaje')
    list_filter = ('contrato', 'fecha','aplicabilidad')

class DescuentoNinAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'tipo_habitacion','porcentaje', 'porcentaje_2','porcentaje_3')
    list_filter = ('contrato','tipo_habitacion', 'fecha_inicio',)


class RestriccionOcupacionAdmin(admin.ModelAdmin):
     list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'tipo_habitacion',
                     'minimo_adultos', 'maximo_adultos', 'maximo_nins',)
     list_filter = ('contrato', 'tipo_habitacion', 'fecha_inicio')

class RestriccionBlackoutAdmin(admin.ModelAdmin):
     list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'minimo_dias',)
     list_filter = ('contrato', 'fecha_inicio')


class RestriccionEstanciaMinimaAdmin(admin.ModelAdmin):
     list_display = ('contrato', 'fecha_inicio', 'fecha_fin', 'minimo_noches','maximo_noches',)
     list_filter = ('contrato', 'fecha_inicio')



admin.site.register(TipoHabitacion, TipoHabitacionAdmin)
admin.site.register(Regimen, RegimenAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(CondicionesContrato, CondicionesContratoAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(SuplementoRegimen, SuplementoRegimenAdmin)
admin.site.register(SuplementoOcupacion, SuplementoOcupacionAdmin)
admin.site.register(RestriccionOcupacion, RestriccionOcupacionAdmin)
admin.site.register(SuplementoDia, SuplementoDiaAdmin)
admin.site.register(RestriccionBlackout, RestriccionBlackoutAdmin)
admin.site.register(RestriccionEstanciaMinima, RestriccionEstanciaMinimaAdmin)
admin.site.register(DescuentoNin, DescuentoNinAdmin)
