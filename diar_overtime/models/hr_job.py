from odoo import models, api, fields


class hr_job(models.Model):
    _inherit = 'hr.job'

    sop_details = fields.Text('SOP Details')