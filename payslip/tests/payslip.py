#!/usr/bin/env python
from unittest import TestCase
from payslip.payslip import migrate_db, destroy,get_monthly_income_tax


# Note(Aaron) need to cover more methods in future
class PayslipTestCase(TestCase):
    def setUp(self):
        migrate_db()

    def test_get_monthly_income_tax(self):
        self.assertEqual(get_monthly_income_tax(60000), 500)

    def tearDown(self):
        destroy()
