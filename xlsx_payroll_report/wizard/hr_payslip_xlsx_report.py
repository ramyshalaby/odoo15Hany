# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, _, fields


class SalaryRuleInput(models.TransientModel):
    _name = 'hr.payslip.xlsx.report'

    hr_payslip_ids = fields.Many2many('hr.payslip', string='Payslips')


    def print_payslip_elsx(self):
        return self.env.ref('xlsx_payroll_report.payroll_excel_report').report_action(self, data={'payslip_list': self.hr_payslip_ids.ids})
        return True