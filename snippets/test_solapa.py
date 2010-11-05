#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from solapa import *

def test_overlaps():
    items = [
      ('First is on the far left ', (1, 2), (8, 9), False),
      ('First is on the far right', (8, 9), (1, 2), False),
      ('Identical ', (1, 9), (1, 9), True),
      ('Same start ',(1, 5), (1, 9), True),
      ('Same end ',  (1, 9), (5, 9), True),
      ('First contains second ', (1, 9), (3, 7), True),
      ('Second contains first ', (3, 7), (1, 9), True),
      ('First end within second ', (1, 7), (3, 9), True),
      ('First start within second', (3, 9),(1, 7), True),
      ('First continues to second', (1, 5),(5, 9), True),
      ('Second continues to first', (5, 9), (1, 5), True),
    ]   
    for s, r1, r2, rta in items:
        assert overlaps (r1, r2)== rta , s

def test_intersects():
    items = [
      ('First is on the far left ', (1, 2), (8, 9), False),
      ('First is on the far right', (8, 9), (1, 2), False),
      ('Identical ', (1, 9), (1, 9), True),
      ('Same start ',(1, 5), (1, 9), True),
      ('Same end ',  (1, 9), (5, 9), True),
      ('First contains second ', (1, 9), (3, 7), True),
      ('Second contains first ', (3, 7), (1, 9), True),
      ('First end within second ', (1, 7), (3, 9), True),
      ('First start within second', (3, 9),(1, 7), True),
      ('First continues to second', (1, 5),(5, 9), True),
      ('Second continues to first', (5, 9), (1, 5), True),
    ]   
    for s, r1, r2, rta in items:
        assert intersects (r1[0], r1[1], r2[0], r2[1])== rta , s
