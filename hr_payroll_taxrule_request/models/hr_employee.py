# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2020-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################


from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def calculate_egypt_icome_tax(self, amount):
        annual_salary = (amount * 12)
        tax_amounts = 0.0
        for tax_levels_obj in  self.env['tax.income.levels'].search([]):
            if annual_salary >= tax_levels_obj.level_max :
                tax_amounts += tax_levels_obj.level_max * tax_levels_obj.level_percentage / 100
                annual_salary = annual_salary - tax_levels_obj.level_max
            elif tax_levels_obj.last_level:
                tax_amounts += annual_salary * tax_levels_obj.level_percentage / 100

        if tax_amounts:
            return tax_amounts /12
        return tax_amounts
