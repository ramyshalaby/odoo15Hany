# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class request_for_information_log(models.Model):
    _name = 'request.for.information.log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Request For Information Log - Structural Works"

    name = fields.Char('Name', track_visibility='always')
    project_id = fields.Many2one('project.project', 'Project', track_visibility='always')
    partner_id = fields.Many2one('res.partner', related="project_id.partner_id", string='Project Customer(Owner)')
    contract_type_id = fields.Many2one('contract.type', 'Contract Type', track_visibility='always')
    project_start_date = fields.Date('Start Date', track_visibility='always')
    project_end_date = fields.Date('End Date', track_visibility='always')
    project_code = fields.Char('Project Code', track_visibility='always')
    diar_scope = fields.Text('Diar Scope', track_visibility='always')
    main_contractor_res_partner_id = fields.Many2one('res.partner', 'Main Contractor', track_visibility='always')
    contractor_res_partner_id = fields.Many2one('res.partner', 'Contractor', track_visibility='always')
    main_consultant_res_partner_id = fields.Many2one('res.partner', 'Main Consultant', track_visibility='always')
    consultant_res_partner_id = fields.Many2one('res.partner', 'Consultant', track_visibility='always')
    last_update = fields.Datetime('Last Update', track_visibility='always')
    request_for_information_log_details_ids = fields.One2many('request.for.information.log.details', 'request_for_information_log_id',
                                                         'Inspection Request Logs')

    h_co_action_code = fields.Integer('Under Approval', compute="calc_acion_code")
    a_co_action_code = fields.Integer('Approval', compute="calc_acion_code")
    b_co_action_code = fields.Integer('Approved With Comments', compute="calc_acion_code")
    c_co_action_code = fields.Integer('Revise And Resubmit', compute="calc_acion_code")
    d_co_action_code = fields.Integer('Rejected', compute="calc_acion_code")
    cancel_co_action_code = fields.Integer('Cancelled', compute="calc_acion_code")
    revision_co_action_code = fields.Integer('Revision', compute="calc_acion_code")

    latest_dos = fields.Integer('Latest Documents', compute="calc_acion_code")
    superseded_dos = fields.Integer('Superseded Documents', compute="calc_acion_code")
    opened_dosStatus = fields.Integer('Opened Documents', compute="calc_acion_code")
    closed_dosStatus = fields.Integer('Closed Documents', compute="calc_acion_code")

    def return_is_top_manager(self):
        if self.user_has_groups('diar_project_dashboard.group_project_dashboard_doc_submittal_log_top_manager'):
            return True
        else:
            return False

    is_top_manager = fields.Boolean('Top Manager', compute="check_is_top_manager", default=return_is_top_manager)

    def check_is_top_manager(self):
        for record in self:
            if self.user_has_groups('diar_project_dashboard.group_project_dashboard_doc_submittal_log_top_manager'):
                record.is_top_manager = True
            else:
                record.is_top_manager = False

    def calc_acion_code(self):
        for record in self:
            record.h_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfi_latest_super == 'latest')))
            record.superseded_dos = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfi_latest_super == 'superseded')))
            record.opened_dosStatus = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfiStatus == 'opened')))
            record.closed_dosStatus = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfiStatus == 'closed')))

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('request.for.information.log') or ' '
        return super(request_for_information_log, self).create(vals)

    def write(self, vals):
        vals['last_update'] = fields.Datetime.now()
        return super(request_for_information_log, self).write(vals)

    @api.onchange('project_id')
    def onchange_project_id(self):
        for record in self:
            if record.project_id:
                record.project_start_date = record.project_id.date_start
                record.project_end_date = record.project_id.date
                # record.project_code = record.project_id.date


class request_for_information_log_details(models.Model):
    _name = 'request.for.information.log.details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Inspection Request Log Details"

    request_for_information_log_id = fields.Many2one('request.for.information.log', 'Inspection Request Log')

    reference = fields.Char('RFI Submittal Ref.', track_visibility='always')
    review = fields.Char('Submittal Rev..', track_visibility='always')
    from_res_partner_id = fields.Many2one('res.partner', 'From The sender')
    to_res_partner_id = fields.Many2one('res.partner', 'To The recipient')
    discipline_section_id = fields.Many2one('discipline.section', 'Discipline', track_visibility='always')
    location_Level = fields.Char("Location/Level", track_visibility='always')
    name = fields.Char('Subject', track_visibility='always')
    description = fields.Text('Description', track_visibility='always')
    copy_type = fields.Selection([('hard', 'Hard'), ('soft', 'Soft')], 'Copy Type', track_visibility='always')
    sentdate = fields.Date('Sent Date ', track_visibility='always')
    duedate = fields.Date('Due Date ', track_visibility='always')
    receiveddate = fields.Date('Received Date ', track_visibility='always')
    replyduration = fields.Integer('Reply Duration', compute="calc_replyduration", track_visibility='always')
    action_code = fields.Selection(
        [('h', 'H'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('cancelled', 'Cancelled'),
         ('revision', 'Revision')], 'RFI Action Code', track_visibility='always')
    submittedfor = fields.Char('Submitted For', track_visibility='always')
    rfi_latest_super = fields.Selection([('latest','Latest'),('superseded','Superseded')],'RFI Latest / Superseded', track_visibility='always')
    rfiStatus = fields.Selection([('opened','Opened'),('closed','Closed')],'RFI Status', track_visibility='always')
    native_file = fields.Binary('Native File', track_visibility='always')
    native_file_name = fields.Char('Native File', track_visibility='always')
    scan_file = fields.Binary('Scan File', track_visibility='always')
    scan_file_name = fields.Char('Scan File', track_visibility='always')
    res_country_id = fields.Many2one('res.country','Country', track_visibility='always')
    packageType = fields.Char('Package Type', track_visibility='always')
    scope = fields.Char('Scope', track_visibility='always')
    notes = fields.Text('Notes', track_visibility='always')

    @api.onchange('action_code','rfi_latest_super')
    def onchange_code_dos(self):
        for record in self:
            if record.action_code == 'h':
                record.rfiStatus = 'opened'
            elif record.action_code == 'c' and record.rfi_latest_super == 'latest':
                record.rfiStatus = 'opened'
            else:
                record.rfiStatus = 'closed'
            if record.action_code:
                record.receiveddate = datetime.now()

    @api.onchange('action_code')
    def onchange_action_code(self):
        for record in self:
            if record.action_code == 'h':
                record.submittedfor = 'Under Approval'
            elif record.action_code == 'a':
                record.submittedfor = 'Approved'
            elif record.action_code == 'b':
                record.submittedfor = 'Approved With Comments'
            elif record.action_code == 'c':
                record.submittedfor = 'Revise And Resubmit'
            elif record.action_code == 'd':
                record.submittedfor = 'Rejected'
            elif record.action_code == 'cancelled':
                record.submittedfor = 'Cancelled'
            elif record.action_code == 'revision':
                record.submittedfor = 'Revision'

    @api.constrains()
    def check_dates(self):
        for record in self:
            if record.sentdate and record.receiveddate and record.receiveddate < record.sentdate:
                raise ValidationError(_("Sorry send date can't exceed received date"))

    @api.depends('sentdate','receiveddate')
    def calc_replyduration(self):
        for record in self:
            record.replyduration = 0
            if record.sentdate and record.receiveddate and record.receiveddate < record.sentdate:
                raise ValidationError(_("Sorry send date can't exceed received date"))
            if record.sentdate and record.receiveddate and record.receiveddate > record.sentdate:
                record.replyduration = (record.receiveddate - record.sentdate).days