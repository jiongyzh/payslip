#!/usr/bin/env python
import uuid
from datetime import datetime
from payslip.models.base import BASE_COLUMNS


def create_table(conn, cur):
    """ Create table tax_rate
     conn: DB Connection
     cur: Cursor
    """
    sql = '''CREATE TABLE IF NOT EXISTS tax_rate (
        {}
        income_from DECIMAL(7,5),
        income_to DECIMAL(7,5),
        rate VARCHAR(255)
      )
    '''.format(BASE_COLUMNS)
    cur.execute(sql)
    conn.commit()
    print('Table tax_rate has been created')


def insert_tax_rate(row, cur):
    """ Insert a row into table tax_rate
     row: Tuple
     cur: Cursor
    """
    sql = '''INSERT INTO tax_rate VALUES(
        ?, ?, ?, ?, ?, ?
      )
    '''
    pk = str(uuid.uuid4())
    timestamp = datetime.now()
    cur.execute(sql, (pk, timestamp, timestamp, row[0], row[1], row[2]))


def get_tax_rates(income, cur):
    """ Get valid rates for a specific income
     income: Int
     cur: Cursor
    """
    sql = '''SELECT income_from, income_to, rate from tax_rate WHERE income_from <= ? ORDER BY income_from'''
    cur.execute(sql, (income,))
    return cur.fetchall()
