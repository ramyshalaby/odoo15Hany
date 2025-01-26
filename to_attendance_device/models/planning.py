from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class PlanningSlot(models.Model):
    _inherit = 'planning.slot'
    def _default_start_datetime(self):
        return fields.Datetime.to_string(datetime.combine(fields.Datetime.now(), datetime.min.time()))

    def _default_end_datetime(self):
        return fields.Datetime.to_string(datetime.combine(fields.Datetime.now(), datetime.max.time()))

    device_start_date=fields.Datetime(required=True,default=_default_start_datetime)
    device_end_date=fields.Datetime(required=True,default=_default_end_datetime)

    @api.onchange('start_datetime','end_datetime')
    def onchange_date(self):
        self.device_start_date=self.start_datetime
        self.device_end_date=self.end_datetime
    @api.model
    def create(self,vals):
        res=super(PlanningSlot, self).create(vals)
        for rec in res:
            rec.device_start_date=rec.start_datetime
            rec.device_end_date=rec.end_datetime
        return res



