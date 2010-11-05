# -*- coding: UTF-8 -*-
# Model para el módulo de contacto

from django.db import models
from django.utils.translation import ugettext as _

class Contacto(models.Model):
    """Modelo para los contactos"""
    nombre = models.CharField(_(u'Nombre'), max_length=200)
    email = models.EmailField(_(u'E-mail'), max_length=200)
    mensaje = models.TextField(_(u'Mensaje'))
    def __unicode__(self):
        return '%s %s' % (self.nombre, self.email)
