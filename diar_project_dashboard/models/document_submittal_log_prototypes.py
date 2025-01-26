# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import io, base64, xlsxwriter, xlwt
from io import StringIO
class document_submittal_log_prototypes(models.Model):
    _name = 'document.submittal.log.prototypes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Project Dashboard Data Protypes"

    document_submittal_log_id = fields.Many2one('document.submittal.log')

    current_wcv = fields.Monetary("Work Completed Value  Accourding to BOQ", currency_field='current_wcv_currency_id')
    current_wcv_currency_id = fields.Many2one('res.currency')
    previous_wcv = fields.Monetary("Work Completed Value  Accourding to BOQ", currency_field="previous_wcv_currency_id")
    previous_wcv_currency_id = fields.Many2one('res.currency')
    current_wpv = fields.Monetary("Work Planned Value  Accourding to BOQ", currency_field="current_wpv_currency_id")
    current_wpv_currency_id = fields.Many2one('res.currency')
    previous_wpv = fields.Monetary("Work Planned Value  Accourding to BOQ", currency_field="previous_wpv_currency_id")
    previous_wpv_currency_id = fields.Many2one('res.currency')
    current_wvcm = fields.Float("Work Value Completed This Month", compute="calc_current_wvcm")
    current_wvpm = fields.Float("Work Value Planned This Month",compute="calc_current_wvpm")
    current_wppp = fields.Float("Work Project Planned Progress This Month", compute="calc_current_wpppm")

    current_ppp = fields.Float("Project Planned Progress")
    current_pppp = fields.Float("Project Planned Progress")

    current_pacp = fields.Float("Project Actual Progress")
    current_ppacp = fields.Float("Project Actual Progress")
    current_wpacp = fields.Float("Work Project Actual Progress This Month", compute="calc_current_wpapm")

    ppptp = fields.Float("Project Planned Progress This Period")
    pcptp = fields.Float("Project Actual Progress This Period")
    oc_date = fields.Date("Original completion date")
    ec_date = fields.Date("Expected completion date")
    project_end_date = fields.Date('Project END Date')
    eoc_variance = fields.Float("Variance", compute="calc_eoc_variance")
    date_variance = fields.Float("Variance", compute="calc_eoc_variance")

    @api.constrains('current_wcv','current_wcv_currency_id','previous_wcv','previous_wcv_currency_id','current_wpv',
                    'current_wpv_currency_id','previous_wpv','previous_wpv_currency_id','current_ppp','current_pppp','ppptp','pcptp','oc_date','ec_date')
    def copy_last_record(self):
        for record in self:
            record.document_submittal_log_id.current_wcv = record.current_wcv
            record.document_submittal_log_id.current_wcv_currency_id = record.current_wcv_currency_id
            record.document_submittal_log_id.previous_wcv = record.previous_wcv
            record.document_submittal_log_id.previous_wcv_currency_id = record.previous_wcv_currency_id
            record.document_submittal_log_id.current_wpv = record.current_wpv
            record.document_submittal_log_id.current_wpv_currency_id = record.current_wpv_currency_id
            record.document_submittal_log_id.previous_wpv = record.previous_wpv
            record.document_submittal_log_id.previous_wpv_currency_id = record.previous_wpv_currency_id
            record.document_submittal_log_id.current_ppp = record.current_ppp
            record.document_submittal_log_id.current_pppp = record.current_pppp
            record.document_submittal_log_id.current_pacp = record.current_pacp
            record.document_submittal_log_id.ppptp = record.ppptp
            record.document_submittal_log_id.pcptp = record.pcptp
            record.document_submittal_log_id.oc_date = record.oc_date
            record.document_submittal_log_id.ec_date = record.ec_date

    @api.onchange('current_wpv', 'previous_wpv')
    @api.depends('current_wpv', 'previous_wpv')
    def calc_current_wvpm(self):
        for record in self:
            record.current_wvpm = record.current_wpv - record.previous_wpv

    @api.onchange('current_wcv', 'previous_wcv')
    @api.depends('current_wcv', 'previous_wcv')
    def calc_current_wvcm(self):
        for record in self:
            record.current_wvcm = record.current_wcv - record.previous_wcv

    @api.onchange('current_ppp', 'current_pppp')
    @api.depends('current_ppp', 'current_pppp')
    def calc_current_wpppm(self):
        for record in self:
            record.current_wppp = record.current_ppp - record.current_pppp

    @api.onchange('current_pacp', 'current_ppacp')
    @api.depends('current_pacp', 'current_ppacp')
    def calc_current_wpapm(self):
        for record in self:
            record.current_wpacp = record.current_pacp - record.current_ppacp


    @api.onchange('ec_date', 'oc_date')
    @api.depends('ec_date','oc_date')
    def calc_eoc_variance(self):
        for record in self:
            record.eoc_variance = 0.0
            record.date_variance = 0.0
            if record.ec_date and record.oc_date and record.ec_date < record.oc_date:
                raise ValidationError(_("Sorry Original completion date can't exceed Expected completion date"))
            if record.ec_date and record.oc_date and record.ec_date > record.oc_date:
                record.eoc_variance = (record.ec_date - record.oc_date).days
            if record.ec_date and record.project_end_date and record.project_end_date > record.ec_date:
                record.date_variance = (record.project_end_date - record.ec_date).days
