# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'TipoHabitacion.maximo_total'
        db.add_column('motor_tipohabitacion', 'maximo_total', self.gf('django.db.models.fields.IntegerField')(default=5), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'TipoHabitacion.maximo_total'
        db.delete_column('motor_tipohabitacion', 'maximo_total')
    
    
    models = {
        'motor.condicionescontrato': {
            'Meta': {'object_name': 'CondicionesContrato'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'cupo': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_apartamento': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_cupo_generado': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_paro_ventas': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_venta_libre': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'regimen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Regimen']"}),
            'tipo_habitacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.TipoHabitacion']"})
        },
        'motor.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'hotel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Hotel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'revisado': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'motor.descuentonin': {
            'Meta': {'object_name': 'DescuentoNin'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limite_bebe': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'limite_nin': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '12'}),
            'porcentaje': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '4', 'decimal_places': '2'}),
            'porcentaje_2': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '4', 'decimal_places': '2'}),
            'porcentaje_3': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '4', 'decimal_places': '2'}),
            'tipo_habitacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.TipoHabitacion']"})
        },
        'motor.hotel': {
            'Meta': {'object_name': 'Hotel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'})
        },
        'motor.inventario': {
            'Meta': {'object_name': 'Inventario'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'cupo_actual': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'cupo_inicial': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'hotel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Hotel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_apartamento': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_paro_ventas': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_venta_libre': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'regimen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Regimen']"}),
            'tipo_habitacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.TipoHabitacion']"})
        },
        'motor.regimen': {
            'Meta': {'object_name': 'Regimen'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_base': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subtipos'", 'null': 'True', 'to': "orm['motor.Regimen']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'})
        },
        'motor.restriccionblackout': {
            'Meta': {'object_name': 'RestriccionBlackout'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimo_dias': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        },
        'motor.restriccionestanciaminima': {
            'Meta': {'object_name': 'RestriccionEstanciaMinima'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximo_noches': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'minimo_noches': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        },
        'motor.restriccionocupacion': {
            'Meta': {'object_name': 'RestriccionOcupacion'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximo_adultos': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'maximo_nins': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'minimo_adultos': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'tipo_habitacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.TipoHabitacion']"}),
            'ventas_sin_limite': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'motor.suplementoocupacion': {
            'Meta': {'object_name': 'SuplementoOcupacion'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcentaje': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '4', 'decimal_places': '2'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'tipo_habitacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.TipoHabitacion']"})
        },
        'motor.suplementoregimen': {
            'Meta': {'object_name': 'SuplementoRegimen'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Contrato']"}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcentaje': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '2'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'regimen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['motor.Regimen']"})
        },
        'motor.tipohabitacion': {
            'Meta': {'object_name': 'TipoHabitacion'},
            'children': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_base': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_individual': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'maximo': ('django.db.models.fields.PositiveIntegerField', [], {'default': '4'}),
            'maximo_total': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'minimo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subtipos'", 'null': 'True', 'to': "orm['motor.TipoHabitacion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['motor']
