# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import ModelForm
from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from contacto.models import Contacto
from captcha.fields import CaptchaField

class ContactoForm(ModelForm):
    class Meta:
        model = Contacto
    captcha = CaptchaField()

def index(request):
    '''Form de petición de contacto '''
    data = {}
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            message = render_to_string('contacto/contacto_mail.txt', {'contacto':contacto})
            send_mail('[MOTOR-HOTELTES] Petición de contacto', message, 'no-reply@apsl.com', settings.EMAIL_CONTACTO)
            return HttpResponseRedirect(reverse('ct-thanks'))
        else: data['form'] = form
    else:
        data['form'] = ContactoForm()
    return render_to_response('contacto/contacto.html', data, context_instance=RequestContext(request))
