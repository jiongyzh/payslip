#!/usr/bin/env python
import sqlite3
from payslip import settings

BASE_COLUMNS = '''
    uuid CHAR(36) PRIMARY KEY,
    created timestamp,
    modified timestamp,
'''

DB_NAME = getattr(settings, 'DB_NAME', 'myob_db')


def connect_db(myob_db=DB_NAME):
    conn = sqlite3.connect(myob_db)
    cur = conn.cursor()
    return conn, cur


def drop_table(table_name, cur):
    """
     table_name: String
     cur: Cursor
    """
    sql = f'''DROP TABLE {table_name}'''
    cur.execute(sql)
    print('Table {} has been dropped'.format(table_name))


def table_exists(table_name, cur):
    """ Check if the table exists
     table_name: String
     cur: Cursor
     return: Boolean
    """
    sql = '''SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?'''
    cur.execute(sql, (table_name,))
    result = cur.fetchone()
    if result:
        return result[0] > 0
    return False
