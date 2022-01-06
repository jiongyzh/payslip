#!/usr/bin/env python

DB_NAME = 'myob_db'

TABLES = ['tax_rate']

TAX_RATES = [
    (0, 20000, 0),
    (20001, 40000, 0.1),
    (40001, 80000, 0.2),
    (80001, 180000, 0.3),
    (180001, None, 0.4)
]
