#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Define las clases que se utilizaran para realizar las consultas de disponiblidad"""
from datetime import timedelta

class Consulta(object):
    def __init__(self, inicio, noches, adultos=2, ninyos=0, num_habitaciones = 1,
                tipo_habitacion = None, hotel = None):
        """inicio es la fecha de entrada
           fin es la fecha de final.
           hotel : es una instalncia de motor.models.Hotel, puede ser None
        """
        self.inicio = inicio
        self.entrada = inicio
        self.fin = inicio + timedelta(days=noches-1)
        self.salida = self.fin + timedelta(days=1)
        self.adultos = adultos
        self.ninyos  = ninyos
        self.num_habitaciones =  num_habitaciones
        self.tipo_habitacion = tipo_habitacion #indica todas
        self.noches = noches
        self.hotel = hotel

    @property
    def ocupacion(self):
        return self.adultos + self.ninyos

    def __str__(self):
        return "(%s - %s :: %s) %s AD %s CH, %s hab de tipo %s Hotel: %s" % ( self.inicio,
                                                             self.fin,
                                                             self.noches,
                                                             self.adultos,
                                                             self.ninyos,
                                                             self.num_habitaciones,
                                                             self.tipo_habitacion if self.tipo_habitacion else "Todas",
                                                             self.hotel_slug if self.hotel_slug else "Todos"           )

#obtener_disponibilidad_inicial(consulta)
