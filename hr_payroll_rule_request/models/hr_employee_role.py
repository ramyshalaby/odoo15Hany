# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrEmployee_payroll_rule(models.Model):
    _name = 'hr.employee.payroll.role'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Payroll Role Request"

    def _get_current_employee(self):
        emp_objs = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)])
        if emp_objs:
            return emp_objs[0].id
        else:
            return {}

    name = fields.Char('Name', track_visibility='always')
    role_group_by = fields.Selection([('departments','Department'), ('tags','Tags'), ('employees','Employees')], track_visibility='always', string=    'Add By')
    department_ids = fields.Many2many('hr.department', string='Departments', track_visibility='always')
    category_ids = fields.Many2many('hr.employee.category', string='Tags', track_visibility='always')
    employee_ids = fields.Many2many('hr.employee', string='Employees', track_visibility='always')

    description = fields.Text('Description')
    applied_date = fields.Date('Applied Date', track_visibility='always')


    role_by = fields.Selection([('fixed', 'Fixed'), ('percentage','Percentage'),('time','Time By Hours'), ('days','Days')], 'By', track_visibility='always')
    role_type = fields.Selection([('allowances','Allowance'), ('deduction', 'Deduction')], 'Type', track_visibility='always')


    fixed_amount = fields.Float('Fixed Amount', track_visibility='always')
    by_percentage_type = fields.Selection([('wage', 'Wage'), ('gross', 'Gross'), ('net', 'Net')], 'Percentage By', track_visibility='always')

    percentage = fields.Float('Percentage', track_visibility='always')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancel', 'cancelled'), ('refused', 'Refused')],
        track_visibility='always', default='draft')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get())

    def confirm_role(self):
        for record in self:
            record.state='confirmed'
        return True
    def cancel_role(self):
        for record in self:
            record.state='cancel'
        return True
    def refuse_role(self):
        for record in self:
            record.state='refused'
        return True
    def back_to_draft(self):
        for record in self:
            record.state='draft'
        return True

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].get('hr.employee.payroll.role') or ' '
        return super(HrEmployee_payroll_rule, self).create(values)