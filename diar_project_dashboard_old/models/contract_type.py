# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class contract_type(models.Model):
    _name = 'contract.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Contract Type"

    name = fields.Char('Name')
    code = fields.Char('Code')
    active = fields.Boolean(default=True)
    description = fields.Text('Description')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Discipline Code Name Already Exist.')
    ]