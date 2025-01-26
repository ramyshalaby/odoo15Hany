# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class discipline_section(models.Model):
    _name = 'discipline.section'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Discipline Section"

    name = fields.Char('Name')
    code = fields.Char('Code')
    active = fields.Boolean(default=True)
    discipline_section_id = fields.Many2one('discipline.section', 'Parent')
    description = fields.Text('Description')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Discipline Code Name Already Exist.')
    ]