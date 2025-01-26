# -*- coding: utf-8 -*-

from dateutil import relativedelta
import pandas as pd
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.resource.models.resource import HOURS_PER_DAY


class social_insurance(models.Model):
    _name = 'social.insurance'
    _description = "Social Insurance"
    _inherit = ['mail.thread']
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', 'Employee', tracking=True)
    social_insurance_number = fields.Char("Social Insurance Number", tracking=True)
    entrydate = fields.Date('Entry date', tracking=True)
    exirdate = fields.Date('Exit date', tracking=True)
    company_name = fields.Char("Company Name", tracking=True)
    social_insurance_details_ids = fields.One2many('social.insurance.details', 'social_insurance_id', tracking=True)


class social_insurance_details(models.Model):
    _name = 'social.insurance.details'
    _inherit = ['mail.thread']

    social_insurance_id = fields.Many2one('social.insurance', tracking=True)
    basic_salary = fields.Float('Basic Salary', tracking=True)
    subscription_fee = fields.Float('Subscription fees', tracking=True)
    total_wage = fields.Float('Total Wage', tracking=True)