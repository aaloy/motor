# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TipoHabitacion'
        db.create_table('motor_tipohabitacion', (
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=20, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subtipos', null=True, to=orm['motor.TipoHabitacion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('minimo', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('maximo', self.gf('django.db.models.fields.PositiveIntegerField')(default=4)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_individual', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('children', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('is_base', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('motor', ['TipoHabitacion'])

        # Adding model 'Regimen'
        db.create_table('motor_regimen', (
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_base', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subtipos', null=True, to=orm['motor.Regimen'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=10, db_index=True)),
        ))
        db.send_create_signal('motor', ['Regimen'])

        # Adding model 'Hotel'
        db.create_table('motor_hotel', (
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=20, db_index=True)),
        ))
        db.send_create_signal('motor', ['Hotel'])

        # Adding model 'Contrato'
        db.create_table('motor_contrato', (
            ('hotel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Hotel'])),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('revisado', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['Contrato'])

        # Adding model 'CondicionesContrato'
        db.create_table('motor_condicionescontrato', (
            ('regimen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Regimen'])),
            ('is_cupo_generado', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('cupo', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('is_apartamento', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('tipo_habitacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.TipoHabitacion'])),
            ('is_paro_ventas', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_venta_libre', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('motor', ['CondicionesContrato'])

        # Adding model 'SuplementoRegimen'
        db.create_table('motor_suplementoregimen', (
            ('regimen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Regimen'])),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('porcentaje', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['SuplementoRegimen'])

        # Adding model 'SuplementoOcupacion'
        db.create_table('motor_suplementoocupacion', (
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('tipo_habitacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.TipoHabitacion'])),
            ('porcentaje', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['SuplementoOcupacion'])

        # Adding model 'DescuentoNin'
        db.create_table('motor_descuentonin', (
            ('limite_nin', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=12)),
            ('porcentaje_2', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=2)),
            ('porcentaje_3', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=2)),
            ('limite_bebe', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('tipo_habitacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.TipoHabitacion'])),
            ('porcentaje', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['DescuentoNin'])

        # Adding model 'RestriccionEstanciaMinima'
        db.create_table('motor_restriccionestanciaminima', (
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('minimo_noches', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('maximo_noches', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['RestriccionEstanciaMinima'])

        # Adding model 'RestriccionOcupacion'
        db.create_table('motor_restriccionocupacion', (
            ('ventas_sin_limite', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('maximo_nins', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('minimo_adultos', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('maximo_adultos', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('tipo_habitacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.TipoHabitacion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('motor', ['RestriccionOcupacion'])

        # Adding model 'RestriccionBlackout'
        db.create_table('motor_restriccionblackout', (
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('minimo_dias', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
        ))
        db.send_create_signal('motor', ['RestriccionBlackout'])

        # Adding model 'Inventario'
        db.create_table('motor_inventario', (
            ('regimen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Regimen'])),
            ('cupo_inicial', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('is_paro_ventas', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('hotel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Hotel'])),
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('is_apartamento', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.Contrato'])),
            ('tipo_habitacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motor.TipoHabitacion'])),
            ('cupo_actual', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_venta_libre', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('motor', ['Inventario'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TipoHabitacion'
        db.delete_table('motor_tipohabitacion')

        # Deleting model 'Regimen'
        db.delete_table('motor_regimen')

        # Deleting model 'Hotel'
        db.delete_table('motor_hotel')

        # Deleting model 'Contrato'
        db.delete_table('motor_contrato')

        # Deleting model 'CondicionesContrato'
        db.delete_table('motor_condicionescontrato')

        # Deleting model 'SuplementoRegimen'
        db.delete_table('motor_suplementoregimen')

        # Deleting model 'SuplementoOcupacion'
        db.delete_table('motor_suplementoocupacion')

        # Deleting model 'DescuentoNin'
        db.delete_table('motor_descuentonin')

        # Deleting model 'RestriccionEstanciaMinima'
        db.delete_table('motor_restriccionestanciaminima')

        # Deleting model 'RestriccionOcupacion'
        db.delete_table('motor_restriccionocupacion')

        # Deleting model 'RestriccionBlackout'
        db.delete_table('motor_restriccionblackout')

        # Deleting model 'Inventario'
        db.delete_table('motor_inventario')
    
    
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
            'minimo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subtipos'", 'null': 'True', 'to': "orm['motor.TipoHabitacion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['motor']
