#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Definición de la Base de datos para el motor de reservas.
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from motor.core.interval import overlaps_in_range, inside
from motor.core.inventario import crear_inventario, crear_inventario_condicion


class TipoHabitacionManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug = slug)

class RegimenManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug = slug)

class TipoHabitacion(models.Model):
    """Define los tipos de habitacion posibles. Una habitación se define
    por su ocupación mínima y máxima.

    Si una habitación es de un tipo base indica que habrá un contrato con
    cupo y precios especiales para este tipo de habitación

    """

    #TODO Añadir anidamento de tipos

    objects  = TipoHabitacionManager()

    slug = models.SlugField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    minimo = models.PositiveSmallIntegerField(default=2, help_text = "Ocupación mínima Adultos")
    maximo = models.PositiveIntegerField(default=4, help_text= "Ocupación máxima adultos")
    children = models.IntegerField(default=2, help_text= "Máxima ocupación de niños")
    maximo_total = models.IntegerField(default=5, help_text = "Ocupación máxima entre adultos y niños")
    is_base = models.BooleanField(help_text = "Marcar si es un referencia para cupo y precio")
    is_individual = models.BooleanField(default=False, help_text="Indica si se refere a ocupación individual")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subtipos',  limit_choices_to={'is_base': True})


    class Meta:
        verbose_name = "Tipo de Habitación"
        verbose_name_plural = "Tipos de Habitación"

    def __unicode__(self):
        return self.descripcion

    def clean(self):
        if self.minimo > self.maximo:
            raise ValidationError('La ocupación mínima debe ser menor que la máxima')
        if self.is_individual:
            self.minimo = 1
            self.maximo = 1
        if self.is_base and (not self.parent==None):
            raise ValidationError('Una habitación base no puede estar ligada a otra')
        if not self.is_base and (self.maximo != self.minimo):
            raise ValidationError('No puede existir rango para habitaciones que no son de tipo base')
        if not self.is_base and (self.parent.maximo < self.minimo):
            raise ValidationError('El máximo no puede superar al de la habitación base')

    def is_valid(self, adultos, ninyos):
        """Dado un número de adultos y niños determina
        si pueden estar en la habitación"""
        return (adultos<=self.maximo) and (adultos>=self.minimo) \
                and (ninyos>=0) and (ninyos<=self.children) \
                and (self.maximo_total >= (adultos+ninyos))

    def natural_key(self):
        return (self.slug, )


class Regimen(models.Model):
    """Definición del régimien alimenticio"""
    slug = models.SlugField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=100)
    is_base = models.BooleanField(help_text="Marcar si es una referencia para cupo y precio")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subtipos')

    objects = RegimenManager()

    class Meta:
        verbose_name="Régimen"
        verbose_name_plural="Regimenes"

    def __unicode__(self):
        return self.descripcion

    def clean(self):
        if self.is_base and (not self.parent==None):
            raise ValidationError('Una habitación base no puede estar ligada a otra')

    def natural_key(self):
        return (self.slug, )

class Hotel(models.Model):
    """Definición del hotel.
    Las habitaciones y régimenes se definen a partir de las condiciones del contrato
    """

    slug = models.SlugField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"

    def __unicode__(self):
        return self.nombre

    def natural_key(self):
        return (self.slug, )

    def get_contrato_html(self, plantilla="contrato.html"):
        """Devuelve la representación del contrato del hotel
        en formato html"""
        from motor.core.contrato import get_contratos
        return get_contratos(self.pk)

class Contrato(models.Model):
    """Contrato.
    Un contra siempre tiene unas fiechas fijas y se refiere
    a un hotel en concreto. La desactivación de un contrato implica que las
    habitaciones del hotel dejan de estar disponibles.

    Importante: para un mismo hotel los contratos no pueden solaparse
    """

    #TODO añadir mercado

    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField()
    hotel        = models.ForeignKey(Hotel)
    activo       = models.BooleanField(default=False,
                                       help_text="Marque com activo para que se genere el cupo")
    revisado     = models.BooleanField(default=False,
                                       help_text="Marque como revisado cuando esté acabado")

    class Meta:
        verbose_name= "Contrato"
        verbose_name_plural = "Contratos"

    def __unicode__(self):
        return "%s [%s]" % (self.nombre, self.hotel)

    def save(self, *k, **kw):
        super(Contrato, self).save(*kw, **kw)

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        contratos = Contrato.objects.filter(hotel=self.hotel, activo=True)
        if self.id:
            contratos = contratos.exclude(pk=self.pk)
        if overlaps_in_range(contratos, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Los contratos para este hotel se solapan")
        if not self.revisado and self.activo:
            raise ValidationError("Un contrato no puede ser activado si no se marca como revisado")

class CondicionesContrato(models.Model):
    """Las condiciones del contrato una vez establecidas y con el contrato
    validado no se pueden modificar, ya que afectaría a cupo y precios."""

    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    regimen = models.ForeignKey(Regimen, limit_choices_to={'is_base': True})
    tipo_habitacion = models.ForeignKey(TipoHabitacion, limit_choices_to={'is_base': True})
    precio = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Precio por persona y noche")
    is_apartamento = models.BooleanField(default=False, help_text="Marcado aplica sólo precio por noche")
    cupo = models.PositiveSmallIntegerField()
    is_paro_ventas = models.BooleanField(default=False,
                                        help_text="Indique si es un paro de ventas")
    is_venta_libre = models.BooleanField(default=False,
                                         help_text="Indique si es venta libre (sin cupo)")
    is_cupo_generado = models.BooleanField(default=False, editable=False)

    def clean(self):
        """
        La fecha de inicio debe ser mayor que la final.
        Las fectas debe estar dentro del rango del contrato
        Las fechas no deben solaparse para un mismo tipo y régimen
        El precio debe ser mayor que cero.
        """
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = CondicionesContrato.objects.filter(contrato=self.contrato,
                                                         regimen=self.regimen,
                                                         tipo_habitacion=self.tipo_habitacion)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este contrato se solapan")
        if self.precio <=0 and not self.is_paro_ventas:
            raise ValidationError("El precio debe ser mayor que cero si no hay paro de ventas")

# suplementos -----------------------------------------------------------------

class SuplementoRegimen(models.Model):
    """Define los suplementos de régimen que se aplicarán al contrato en las fechas
    determinadas tomando como base el régimen padre

    suplemento = regimen.precio + suplemento.precio + regimen.precio*porcentaje%

    Por ejemplo, si el precio por pesona y noche en MP para habitación doble std es 20
    y tenemos un suplemento de pensión completa de 10 + 5% el total sería

    total = 20 + 10 + 20*0.05 = 31

    Si no hay suplementos de régimen definidos se supone que dicho régimen no está
    definido para ese contrato en esas fechas.

    """
    hotel = models.ForeignKey(Hotel)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    regimen = models.ForeignKey(Regimen, limit_choices_to={'is_base': False})
    precio = models.DecimalField("sobre precio", max_digits = 5, decimal_places = 2, help_text="Suplemento absoluto sobre persona y noche")
    class Meta:
        verbose_name = u"Suplemento de Régimen"
        verbose_name_plural = u"Suplementos de Régimen"

    def clean(self):
        """Las fechas para un mismo contrato y regimen no pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = SuplementoRegimen.objects.filter(hotel=self.hotel,
                                                         regimen=self.regimen)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este suplemento se solapan")

    @classmethod
    def tipos(cls):
        """Devuelve los identificadores de los tipos de suplementos que tenemos definidos
        en el sistema"""
        return SuplementoRegimen.objects.all().distinct().values_list('regimen', flat=True)

class SuplementoOcupacion(models.Model):
    """Define los suplementos de régimen que se aplicarán al contrato en las fechas
    determinadas tomando como base el régimen padre

    suplemento = regimen.precio + suplemento.precio + regimen.precio*porcentaje%

    Por ejemplo, si el precio por pesona y noche en MP para habitación doble std es 20
    y tenemos un suplemento de habitació individual de 10 + 5% el total sería

    total = 20 + 10 + 20*0.05 = 31

    """
    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_habitacion = models.ForeignKey(TipoHabitacion, limit_choices_to={'is_base': False})
    precio = models.DecimalField("sobre precio", max_digits = 5, decimal_places = 2, help_text="Suplemento absoluto sobre persona y noche")
    porcentaje = models.DecimalField(max_digits=4, decimal_places=2, default=0.0,
                                     help_text="Suplemento en % sobre persona y noche, ejemplo: 0.10=10%")

    class Meta:
        verbose_name = u"Suplemento de Ocupación"
        verbose_name_plural = u"Suplementos de Ocupación"

    def clean(self):
        """Las fechas para un mismo contrato y tipo de habitación no pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = SuplementoOcupacion.objects.filter(contrato=self.contrato,
                                                         tipo_habitacion=self.tipo_habitacion)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este suplemento se solapan")


APLICABILIDAD = (
                    ('A', 'Adultos'),
                    ('N', 'Niños'),
                    ('T', 'Todos')
                )
class SuplementoDia(models.Model):
    """Permite aplicar suplementos (o descuentos)
    en días concretos"""
    contrato = models.ForeignKey(Contrato)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=5, decimal_places=2,
                                   help_text="suplememento absoluto sobre la reserva")
    aplicabilidad=models.CharField(max_length=1, choices = APLICABILIDAD)
    porcentaje = models.DecimalField(max_digits=4, decimal_places=2, default=0.0,
                                 help_text="Suplemento en tanto por ciento")

    class Meta:
        verbose_name = u"Suplemento Día"
        verbose_name_plural = u"Suplementos Día"

    def __unicode__(self):
        return u"%s %s %s %s" % (self.fecha, self.descripcion, self.precio,
                                self.aplicabilidad)


    def __str__(self):
        return "%s %s %s %s" % (self.fecha, self.descripcion, self.precio,
                                self.aplicabilidad)
#---------------------------------------------------------------------------
# Descuentos
#---------------------------------------------------------------------------

class DescuentoNin(models.Model):
    """Gestiona los descuentos aplicados por tipo de habitación según los niños
    y la fecha.
    Los descuentos pueden ser distintos por tipo de habitación y fecha pero
    siempres se aplicarán sobre el precio final del adulto.
    """

    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_habitacion = models.ForeignKey(TipoHabitacion,
                                        limit_choices_to={'is_individual': False})
    porcentaje = models.DecimalField("dto 1er niño" , max_digits=4, decimal_places=2, default=0.0,
                                     help_text="Descuento sobre el precio total de adulto del primer niño. Ej. 0.5 = 50%")

    porcentaje_2 =  models.DecimalField("dto. 2o niño", max_digits=4, decimal_places=2, default=0.0,
                                     help_text="Descuento sobre el precio total de adulto del segundo niño. Ej. 0.5 = 50%")

    porcentaje_3 =  models.DecimalField("dto 3r niño", max_digits=4, decimal_places=2, default=0.0,
                                     help_text="Descuento sobre el precio total de adulto del tercer niño y siguientes. Ej. 0.5 = 50%")


    class Meta:
        verbose_name = "Descuento niño"
        verbose_name_plural = "Descuento niños"

    def clean(self):
        """Las fechas para un mismo contrato pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = DescuentoNin.objects.filter(contrato=self.contrato,
                                                         tipo_habitacion=self.tipo_habitacion)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este suplemento se solapan")

    def descuento(self, ninyos):
        """Devuelve suma de descuentos. Los descuentos van sobre
        el precio de adulto por lo que se pueden sumar, de modo que
        el dto total es:
            precio_adulto*ninyos*sum(porcentaje_i)

        donde i=1..ninyos

        """
        return sum((self.porcentaje, self.porcentaje_2, self.porcentaje_3)[0:ninyos])


# ----------------------------------------------------------------------------------
# Restricciones a la venta
#------------------------------------------------------------------------------------
class RestriccionEstanciaMinima(models.Model):
    """Para unas fechas concretas nos puede interesar no vender si no es con
    una estancia mímima y/o máxima.
    """

    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    minimo_noches = models.PositiveSmallIntegerField(default=2,
                                                   help_text="Estancia mínima en la que se puede reservar")
    maximo_noches = models.PositiveSmallIntegerField(default=30,
                                                   help_text="Máximo número de noches que puede estar en el hotel")

    class Meta:
        verbose_name = "Restricción estancia mínima"
        verbose_name_plural = "Restricciones estancia mínima"

    def clean(self):
        """Las fechas para un mismo contrato pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = RestriccionEstanciaMinima.objects.filter(contrato=self.contrato)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para esta restricción se solapan")
        if  self.minimo_noches > self.maximo_noches:
            raise ValidationError('El mínimo de noches debe ser inferior al máximo')

    def is_valid(self, noches):
        return (noches <= self.maximo_noches) and (noches >= minimo_noches)


class RestriccionOcupacion(models.Model):
    """Permite indicar para un contrato las restricciones de ocupación de un tipo de habitación
    Los tipos de habitación serán base. Así para indicar que no queremos vender dobles en usu
    individual en un rango de fechas, bastará que le asignemos una ocupación minima de 2 adultos.
    x = RestriccionOcupacion.objects.filter(contrato__pk=contrato).exclude(
        Q(fecha_inicio__gt=fin)|Q(fecha_fin__lt=inicio))
    """

    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_habitacion = models.ForeignKey(TipoHabitacion, limit_choices_to={'is_base': True})
    minimo_adultos = models.PositiveSmallIntegerField(default=2,
                                                   help_text="Mínimo número de adultos permitidos")
    maximo_adultos = models.PositiveSmallIntegerField(default=4,
                                                   help_text="Máximo número de adultos permitidos")
    maximo_nins = models.PositiveSmallIntegerField(default=2,
                                                   help_text="Máximo número de niños permitidos")

    #ventas_sin_limite = models.PositiveSmallIntegerField(default=0,
    #                                               help_text="Indica el número máximo de ventas que se permiten antes de aplicar la restricción")

    class Meta:
        verbose_name = "Restriccion de ocupación"
        verbose_name_plural= "Restricciones de ocupación"

    def clean(self):
        """Las fechas para un mismo contrato pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = RestriccionOcupacion.objects.filter(contrato=self.contrato, tipo_habitacion=self.tipo_habitacion)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este suplemento se solapan")
        if not inside((self.contrato.fecha_inicio, self.contrato.fecha_fin,), \
                      (self.fecha_inicio, self.fecha_fin)):
            raise ValidationError('Las fechas deben corresponder con las del contrato')
        if  self.minimo_adultos > self.maximo_adultos:
            raise ValidationError('El mínimo de adultos debe ser inferior al máximo')

    def is_restriccion(self, adultos, ninyos):
        """Dado un número de adultos y niños determina
        si pueden estar en la habitación"""
        return (adultos>self.maximo_adultos) or \
                (adultos<self.minimo_adultos) or \
                (ninyos<0) or (ninyos>self.maximo_nins)



class RestriccionBlackout(models.Model):
    """Indica los días mínimos de antelación con los que debe llegar una reserva"""

    contrato = models.ForeignKey(Contrato)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    minimo_dias = models.PositiveSmallIntegerField(default=2,
                                                   help_text="Mínimo número de días de antelación")

    class Meta:
        verbose_name = "Restricción Blackout"
        verbose_name_plural="Restricciones Blackout"

    def clean(self):
        """Las fechas para un mismo contrato pueden solaparse"""
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha fin debe ser mayor que la inicial")
        condiciones = RestriccionBlackout.objects.filter(contrato=self.contrato)
        if self.id:
            condiciones = condiciones.exclude(pk=self.pk)
        if overlaps_in_range(condiciones, self.fecha_inicio, self.fecha_fin,
                                         lambda x: (x.fecha_inicio, x.fecha_fin)):
            raise ValidationError("Las condiciones para este suplemento se solapan")


#--------------------------------------------------------------------------------------------------
# Inventario
# -------------------------------------------------------------------------------------------------

class Inventario(models.Model):
    """El inventario es la tabla desnormalizada en la que se guarda
    el cupo disponible para cada hotel"""
    hotel = models.ForeignKey(Hotel)
    contrato = models.ForeignKey(Contrato)
    fecha = models.DateField()
    regimen = models.ForeignKey(Regimen)
    tipo_habitacion = models.ForeignKey(TipoHabitacion)
    cupo_inicial = models.PositiveSmallIntegerField()
    cupo_actual = models.PositiveSmallIntegerField()
    precio =  models.DecimalField(max_digits = 5, decimal_places = 2)
    is_apartamento = models.BooleanField()
    is_paro_ventas = models.BooleanField()
    is_venta_libre = models.BooleanField()

    def __str__(self):
        return "H: %(hotel)s Hab: %(regimen)s %(tipo)s Cupo %(cupo)s" % \
            {'hotel': self.hotel,
             'regimen':self.regimen,
             'tipo':self.tipo_habitacion,
             'cupo': self.cupo_actual}

# signals
# ------------------

def llenar_inventario(sender, **kwargs):
    """Cuando se guarda un contrato comprobaremos que
    se ha activado y en este caso generaremos las entradas de inventario"""
    contrato = kwargs['instance']
    created = kwargs['created']
    if contrato.revisado and contrato.activo:
        crear_inventario(contrato)

post_save.connect(llenar_inventario, sender=Contrato)

def llenar_inventario_condicion(sender, **kwargs):
    """Cuando se guarda una nueva condición asociada a un contrato, comprobaremos
    que el contrato está revisado y activo y podemos generar la entrada de inventario
    si no se había hecho ya"""
    condicion = kwargs['instance']
    created = kwargs['created']
    if created:
        crear_inventario_condicion(condicion)
post_save.connect(llenar_inventario_condicion, sender=CondicionesContrato)
