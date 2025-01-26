# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, _, fields


class hr_employee(models.Model):
    _inherit = 'hr.employee'
    payment_method = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], string='Payment Type')
    bank_account_id2 = fields.Many2one("res.bank","Bank")
    bank_account_number = fields.Char("Account No")
    bank_account_iban_number = fields.Char("IBAN Account No")

class hr_contract(models.Model):
    _inherit = 'hr.contract'
    payment_method = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], related="employee_id.payment_method", string='Payment Type')

class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'
    payment_method = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], related="employee_id.payment_method", string='Payment Type')
    def action_bulk_xlsx_payslip_report(self):
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payslip Report'),
            'res_model': 'hr.payslip.xlsx.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids':self.ids, 'default_hr_payslip_ids': self.env.context.get('active_ids')}
        }

    def print_payslip_elsx(self):
        # return self.env.ref('xlsx_payroll_report.payroll_excel_report').report_action(self, data={'payslip_list': self.env.context.get('active_ids')})
        return self.env.ref('xlsx_payroll_report.payroll_excel_report').report_action(self, data={'payslip_list': self.ids})
        return True
