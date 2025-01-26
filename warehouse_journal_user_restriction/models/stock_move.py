# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.constrains('state', 'location_id', 'location_dest_id')
    def check_user_location_rights(self):
        for rec in self:
            if rec.state == 'draft':
                return True

            user_locations = []
            for i in rec.env.user.stock_location_ids:
                user_locations.append(i.id)

            # user_locations = rec.env.user.stock_location_ids
            if rec.env.user.restrict_locations:
                message = _(
                    'Invalid Location. You cannot process this move since you do '
                    'not control the location "%s". '
                    'Please contact your Administrator.')

                if rec.location_id.id not in user_locations:
                    raise UserError(message % rec.location_id.name)
                elif rec.location_dest_id.id not in user_locations:
                    raise UserError(message % rec.location_dest_id.name)