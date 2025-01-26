# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class tax_income_levels(models.Model):
    _name = 'tax.income.levels'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Egypt income tax levels"
    _order = "sequence asc"
    _rec_name = "Level_description"


    sequence = fields.Integer('Level Sequence')
    level_min = fields.Float('Level MIN')
    level_max = fields.Float('Level MAX')
    level_percentage = fields.Float('Percentage')
    last_level = fields.Boolean('Last Level')
    Level_description = fields.Text('Description')

    @api.constrains('level_max', 'level_min')
    def check_levels(self):
        for record in self:
            if record.level_min >= record.level_max:
                raise ValidationError(_("Level Minimum can't exceed level maximum"))
            if self.search_count([('level_min','<',record.level_min),('level_max','>',record.level_min), ('id','!=',record.id)]):
                raise ValidationError(_("Sorry This Level exist before"))
            if self.search_count([('level_min', '<', record.level_max), ('level_max', '>', record.level_max), ('id','!=',record.id)]):
                raise ValidationError(_("Sorry This Level exist before"))
            if record.search_count([('last_level','=',True)]) > 2:
                raise ValidationError(_("Sorry anther record with last level please review"))

