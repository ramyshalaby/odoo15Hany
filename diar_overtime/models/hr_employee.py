from odoo import models, api, fields


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    social_insurance_number = fields.Char("Social Insurance Number", tracking=True)
    entrydate = fields.Date('Entry date', tracking=True)
    exirdate = fields.Date('Exit date', tracking=True)
    company_name = fields.Char("Company Name", tracking=True)
    social_insurance_ids = fields.One2many('social.insurance', 'employee_id', 'social_insurance', tracking=True)