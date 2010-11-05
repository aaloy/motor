#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import template
from motor.models import Hotel
import re

register = template.Library()

def check(value):
    if value in ['True', True]:
        return unichr(9745)
    else:
        return unichr(8722);

register.filter('check',check)

def percent(value):
    "Convierte números 0.1 a 10.00 %"
    value = value * 100
    return "%05.2s %%" % value

register.filter('percent', percent)


# get_hotels tag
# obtiene la lista de hoteles

class HotelsNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Hotel.objects.all()
        return ""

@register.tag(name="get_hotels")
def do_get_hotels(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % \
                token.contents.split()[0]
    m = re.search(r'as (?P<var_name>\w+)', arg)
    if not m:
        raise template.TemplaSyntaxError, "%r tag had invalid arguments"  % tag_name
    var_name = m.group('var_name')
    return HotelsNode(var_name)

