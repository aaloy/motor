#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from motor.models import Hotel
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', direct_to_template, {'template':'index.html'},
                                    name='index-recepcion'),
    (r'^hotel/', include('hotel.urls')),
    (r'^recepcion/', include('recepcion.urls')),
    (r'^motor/', include('motor.urls')),
    (r'^contacto/', include('contacto.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    url (
        r'^faq/$',
        'faq.views.faq_list_by_group',
        name = 'faq',
    ),
                       )

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)
# We're going to use the Django server in development, so we'll server
# also the estatic content.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'./media/'}),
    )


