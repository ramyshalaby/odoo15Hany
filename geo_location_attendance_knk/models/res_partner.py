# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from geopy import distance

from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_branch = fields.Boolean(string="Is Branch", )
