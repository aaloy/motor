# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('contacto.views',
   url(r'^$', 'index',name='ct-form'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^thanks/$', 'direct_to_template', {'template': 'contacto/thanks.html'}, name='ct-thanks'),
)
