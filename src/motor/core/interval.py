#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime,timedelta

def datetime_iterator(from_date=datetime.now(), to_date=None):
    """Devuelve un iterador que nos permite construir el
    rango de fechas requerido"""
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 1)
    return



def overlaps_in_range(lista, inicio, fin, f = lambda x: x):
    """
    Devuelve verdadero si el intervalo solapa con alguno de los intervalos
    de la lista.

    f debe ser una función que devuelva un intervalo de fechas com tupla
    """

    for x in lista:
        r = f(x)
        if not ((r[1]<inicio) or (r[0]>fin)):
            return True
    return False

def inside(mayor, menor):
    """Comprueba que intervalo2 está dentro de
    intervalo 1 o bien son iguales"""
    return (mayor[0]<=menor[0]) and (mayor[1]>=menor[1])
