#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#investigación sobre el solapamiento de intervalos

def overlaps(r1,r2):
    """
    siendo r1 y r2 dos intervalos definidos como r1=(x1, y1) y 
    r2 = (x2, y2), donde xi >= yi para i=1,2 entonces decimos que 
    los r1 NO intersecta con r2 sii
        y2 < x1 o x2 > y1
    """
    return not ((r2[1]<r1[0]) or (r2[0]>r1[1]))

def overlaps_in_range(lista, intervalo, f = lambda x: x):
    """
    Devuelve verdadero si el intervalo solapa con alguno de los intervalos
    de la lista
    """
    for x in lista:
        r = f(x)
        if not ((r[1]<intervalo[0]) or (r[0]>intervalo[1])):
            return True
    return False

def intersects(r1start, r1end, r2start, r2end):
    sstart = max(r1start, r2start);
    send = min(r1end, r2end);
    return sstart <= send;

def en_sql():
"""
FECHA_INI FECHA_FIN
26/09/2007 27/11/2007
27/07/2007 26/09/2007
30/05/2007 27/07/2007
19/02/2007 27/03/2007
19/02/2007 30/05/2007

En las dos últimas filas la fecha de inicio es la misma, pero podría darse cualquier tipo de solapamiento.

Solución:

select * from tabla t1, tabla t2
where t2.fecha_ini < t1.fecha_fin
and t2.fecha_fin > t1.fecha_ini
and not t2.rowid = t1.rowid 

Solución 2:

select * from fechas t1, fechas t2
where max(t1.start, t2.start) <= min(t1.end, t2.end)
and not (t1.id = t2.id)

"""