# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from geopy import distance

from odoo import fields, models, _

class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    # active_location = fields.Many2one('res.partner', string=" O Active Location")

    active_location_ids = fields.Many2many('res.partner', string="Active Location",domain="[('is_branch', '=', 'True')]")

    def attendance_location(self, next_action, latitude=None, longitude=None, entered_pin=None):
        self.ensure_one()
        params = self.env['ir.config_parameter'].sudo()
        att_range = int(params.get_param('hr_attendance_location_knk.attendance_range', default=50))
        if latitude is not None and longitude is not None:
            for location in self.active_location_ids:
                act_latitude = location.partner_latitude
                act_longitude = location.partner_longitude
                if act_latitude and act_longitude:
                    pdistance = distance.distance((act_latitude, act_longitude), (latitude, longitude)).km
                    if (pdistance*1000) <= att_range:
                        return self.attendance_manual(next_action=next_action, entered_pin=entered_pin)
            return {'warning': _("You can only do check in/out within Active Location range")}
        return self.attendance_manual(next_action=next_action, entered_pin=entered_pin)
