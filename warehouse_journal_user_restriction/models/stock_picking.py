""" Initialize Internal Transfer """

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('picking_type_id', 'partner_id')
    def _onchange_picking_type(self):
        """ Override _onchange_picking_type """
        res = super(StockPicking, self)._onchange_picking_type()
        return {"domain": {"location_id": [("id", "in", self.env.user.stock_location_ids.ids)]}}
