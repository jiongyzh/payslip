#!/usr/bin/env python
from sqlite3 import OperationalError
from decimal import Decimal, InvalidOperation
from payslip import settings
from payslip.models.base import connect_db, table_exists, drop_table
from payslip.models.tax_rate import create_table as create_table_tax_rate, insert_tax_rate, get_tax_rates

TABLES = getattr(settings, 'TABLES', [])
TAX_RATES = getattr(settings, 'TAX_RATES', [])


def command_help():
    help_str = '''Valid Commands:
    1. Migrate
       -- Create the database and migrate the data, only need to be executed when you run the script first time.

    2. GenerateMonthlyPayslip <employee_name> <annual_salary>
       -- Generate monthly payslip for the input employee, annual_salary has to be a number

    3. Destroy
       -- Drop the created tables

    4. Term
       -- Terminate the script
    '''
    print(help_str)


def migrate_db():
    """ Create tables, then migrate data
    """
    conn, cur = connect_db()
    skip = True
    for table in TABLES:
        if table_exists(table, cur):
            print('Table {} already exists'.format(table))
        else:
            skip = False
    if skip:
        conn.close()
        return

    create_table_tax_rate(conn, cur)
    for rate in TAX_RATES:
        insert_tax_rate(rate, cur)
    conn.commit()
    conn.close()


def destroy():
    conn, cur = connect_db()
    for table in TABLES:
        drop_table(table, cur)
    conn.close()


def are_valid_tax_rates(tax_rates):
    """ Cehck if the input tax rates are valid
     tax_rates: An Array of Tuples
     cur: Cursor
    """
    previous_income_to = -1
    for tax_rate in tax_rates:
        current_income_from = tax_rate[0]
        current_income_to = tax_rate[1]
        if previous_income_to + 1 < current_income_from:
            print('There are gaps between tax rates')
            return False
        if previous_income_to + 1 > current_income_from:
            print('There are overlaps between tax rates')
            return False
        previous_income_to = current_income_to
    return True


def get_monthly_income_tax(salary):
    """ Return monthly income tax based on an annual income
     salary: Decimal
     return: None or Decimal
    """
    conn, cur = connect_db()
    try:
        tax_rates = get_tax_rates(int(salary), cur)
        if not are_valid_tax_rates(tax_rates):
            conn.close()
            return None
        annual_income_tax = Decimal(0)
        for tax_rate in tax_rates:
            income_from = tax_rate[0]
            if income_from == 0:
                income_from += 1
            income_to = tax_rate[1]
            rate = Decimal(tax_rate[2])
            if income_to is not None and salary >= income_to:
                annual_income_tax += (income_to - income_from + 1) * rate
            else:
                annual_income_tax += (salary - income_from + 1) * rate
    except OperationalError as e:
        print(e)
        print('You need to do migrate first')
        conn.close()
        return None
    except InvalidOperation:
        print("tax rate has to be a number")
        conn.close()
        return None
    conn.close()
    return annual_income_tax / 12


def generate_payslip(command):
    """ Generate payslip for an employee
     command: String
    """
    command_split = command.split()
    if len(command_split) != 3:
        print("Your command is invalid, type 'help' to see valid commands")
        return
    try:
        name = command_split[1]
        annual_salary = Decimal(command_split[2])
        gross_monthly_income = annual_salary / 12
        monthly_income_tax = get_monthly_income_tax(annual_salary)
        if monthly_income_tax is None:
            print("type 'help' to see valid commands")
        else:
            net_monthly_income = gross_monthly_income - monthly_income_tax
            payslip = '***\nMonthly Payslip for: {}\nGross Monthly Income: ${}\nMonthly Income Tax: ${}\n' \
                      'Net Monthly Income: ${}\n***'.format(name, '{:.2f}'.format(gross_monthly_income),
                                                            '{:.2f}'.format(monthly_income_tax),
                                                            '{:.2f}'.format(net_monthly_income)
                                                            )
            print(payslip)
    except InvalidOperation:
        print("Annual salary has to be a number, type 'help' to see valid commands")
        return
