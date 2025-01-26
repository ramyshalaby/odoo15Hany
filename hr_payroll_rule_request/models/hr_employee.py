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

    def calculate_allowance_rule_request(self, wage_hour, date_from,date_to, type):
        allowance_payroll_role_objs = self.env['hr.employee.payroll.role'].search([('state','=','confirmed'),('applied_date','>=',date_from),('applied_date','<=',date_to),
                                                                                   '|','|', ('employee_ids','in',self.id),('department_ids','in',self.department_id.id),('category_ids','in',self.category_ids.ids)])
        total_hours = 0.0
        if allowance_payroll_role_objs:
            for allowance_payroll_role_obj in allowance_payroll_role_objs:
                if allowance_payroll_role_obj.role_type == type:
                    if allowance_payroll_role_obj.role_by == 'fixed':
                        total_hours += allowance_payroll_role_obj.fixed_amount
                    elif allowance_payroll_role_obj.role_by == 'percentage':
                        if allowance_payroll_role_obj.by_percentage_type == 'wage':
                            total_hours += self.contract_id.wage*allowance_payroll_role_obj.percentage/100
                        elif allowance_payroll_role_obj.by_percentage_type == 'gross':
                            total_hours += self.contract_id.gross*allowance_payroll_role_obj.percentage/100
                        elif allowance_payroll_role_obj.by_percentage_type == 'net':
                            total_hours += self.contract_id.net*allowance_payroll_role_obj.percentage/100
                    elif allowance_payroll_role_obj.role_by == 'time':
                        total_hours += allowance_payroll_role_obj.fixed_amount * wage_hour
                    elif allowance_payroll_role_obj.role_by == 'days':
                        total_hours += allowance_payroll_role_obj.fixed_amount * wage_hour
            return total_hours
        return 0