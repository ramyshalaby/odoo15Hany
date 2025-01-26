# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import io, base64, xlsxwriter, xlwt
from io import StringIO
from xlrd import open_workbook


# class board_board(models.TransientModel):
#     _inherit = 'board.board'
#
#     display_name = fields.Char()

class document_submittal_log(models.Model):
    _name = 'document.submittal.log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Project Dashboard Data"

    name = fields.Char('Name', track_visibility='always')
    project_id = fields.Many2one('project.project', 'Project', track_visibility='always')
    partner_id = fields.Many2one('res.partner', related="project_id.partner_id", string='Project Customer(Owner)')
    contract_type_id = fields.Many2one('contract.type', 'Contract Type', track_visibility='always')

    Project_Budget = fields.Float("Project Budget (EGP)", track_visibility='always')
    Advance_Payment = fields.Float("Advance Payment (EGP)", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Advance_Payment_Per = fields.Float("Advance Payment %", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Retention_percentage = fields.Float("Retention % ", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Retention = fields.Float("Retention", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)

    @api.depends('Project_Budget', 'Advance_Payment_Per','Advance_Payment','Retention','Retention_percentage')
    def calc_Advance_Payment(self):
        for record in self:
            record.Advance_Payment = record.Project_Budget * record.Advance_Payment_Per
            record.Advance_Payment_Per = (record.Advance_Payment / record.Project_Budget) if record.Advance_Payment > 0.0 and record.Project_Budget > 0.0 else 0.0
            record.Retention = record.Retention_percentage * record.Project_Budget
            record.Retention_percentage = (record.Retention / record.Project_Budget) if record.Retention>0.0 and record.Project_Budget>0.0 else 0.0

    @api.onchange('Project_Budget', 'Advance_Payment_Per','Retention_percentage')
    def onchange_Advance_Payment_Per(self):
        for record in self:
            if record.Project_Budget > 0 and record.Advance_Payment_Per > 0:
                record.Advance_Payment = record.Project_Budget * record.Advance_Payment_Per
            if record.Project_Budget > 0 and record.Retention_percentage > 0:
                record.Retention = record.Project_Budget * record.Retention_percentage
    #
    @api.onchange('Project_Budget', 'Advance_Payment','Retention')
    def onchange_Advance_Payment_Per2(self):
        for record in self:
            if record.Advance_Payment > 0 and record.Project_Budget>0:
                record.Advance_Payment_Per = record.Advance_Payment / record.Project_Budget
            if record.Retention > 0 and record.Project_Budget > 0:
                record.Retention_percentage = record.Retention / record.Project_Budget

    Commencement_Date = fields.Date("Commencement Date", track_visibility='always')
    Project_Duration = fields.Float("Project Duration (Days)", track_visibility='always',compute="calc_projectduration")

    project_start_date = fields.Date('Start Date', track_visibility='always')
    project_end_date = fields.Date('End Date', track_visibility='always')

    @api.depends('project_start_date', 'project_end_date')
    def calc_projectduration(self):
        for record in self:
            record.Project_Duration = 0
            if record.project_start_date and record.project_end_date and record.project_end_date < record.project_start_date:
                raise ValidationError(_("Sorry send date can't exceed received date"))
            if record.project_start_date and record.project_end_date and record.project_end_date > record.project_start_date:
                record.Project_Duration = (record.project_end_date - record.project_start_date).days

    elapsed_time = fields.Float("Elapsed Time %", compute="calc_elapsed_remaiing_time")
    remaining_time = fields.Float("Remaining Time %", compute="calc_elapsed_remaiing_time")
    project_code = fields.Char('Project Code', track_visibility='always')
    diar_scope = fields.Text('Diar Scope', track_visibility='always')
    main_contractor_res_partner_id = fields.Many2one('res.partner', 'Main Contractor', track_visibility='always')
    contractor_res_partner_id = fields.Many2one('res.partner', 'Contractor', track_visibility='always')
    main_consultant_res_partner_id = fields.Many2one('res.partner', 'Main Consultant', track_visibility='always')
    consultant_res_partner_id = fields.Many2one('res.partner', 'Consultant', track_visibility='always')
    from_res_partner_id = fields.Many2one('res.partner', 'From The sender', track_visibility='always')
    to_res_partner_id = fields.Many2one('res.partner', 'To The recipient', track_visibility='always')

    last_update = fields.Datetime('Last Update', track_visibility='always')
    document_submittal_log_details_ids = fields.One2many('document.submittal.log.details', 'document_submittal_log_id',
                                                         'Document Submittal Logs')
    document_submittal_sd_log_details_ids = fields.One2many('document.submittal.sd.log.details',
                                                            'document_submittal_log_id',
                                                            'Document Submittal SD Logs')
    inspection_request_log_details_ids = fields.One2many('inspection.request.log.details', 'document_submittal_log_id',
                                                         'Inspection Request Logs')
    material_inspection_request_log_details_ids = fields.One2many('material.inspection.request.log.details',
                                                                  'document_submittal_log_id',
                                                                  'Material Inspection Request Logs')
    material_submittal_log_details_ids = fields.One2many('material.submittal.log.details', 'document_submittal_log_id',
                                                         'Material Submittal Logs')
    non_conformance_report_log_details_ids = fields.One2many('non.conformance.report.log.details',
                                                             'document_submittal_log_id',
                                                             'Non Conformance Report Logs')
    request_for_information_log_details_ids = fields.One2many('request.for.information.log.details',
                                                              'document_submittal_log_id',
                                                              'Request For Information Logs')
    submittal_log_details_file = fields.Binary('Select File')
    submittal_log_details_file_name = fields.Char()
    submittal_sd_log_details_file = fields.Binary('Select File')
    submittal_sd_log_details_file_name = fields.Char()
    inspection_request_log_details_file = fields.Binary('Select File')
    inspection_request_log_details_file_name = fields.Char('')
    material_inspection_request_log_details_file = fields.Binary('Select File')
    material_inspection_request_log_details_file_name = fields.Char('')
    material_submittal_log_details_file = fields.Binary('Select File')
    material_submittal_log_details_file_name = fields.Char('')
    non_conformance_report_log_details = fields.Binary('Select File')
    request_for_information_log_details_file = fields.Binary('Select File')
    request_for_information_log_details_file_name = fields.Char('')

    NumberofHospitalBeds = fields.Integer('Number of Hospital Beds', track_visibility='always')
    NumberofFloors = fields.Char("Number of Floors", track_visibility='always')
    TotalProjectArea_m2 = fields.Float("Total Project Area (m2)", track_visibility='always')
    document_submittal_log_prototypes_ids = fields.One2many('document.submittal.log.prototypes', 'document_submittal_log_id', 'Prototypes')
    current_wcv = fields.Monetary("Work Completed Value  Accourding to BOQ", currency_field='current_wcv_currency_id')
    current_wcv_currency_id = fields.Many2one('res.currency')
    previous_wcv = fields.Monetary("Previous Work Completed Value  Accourding to BOQ", currency_field="previous_wcv_currency_id")
    previous_wcv_currency_id = fields.Many2one('res.currency')
    current_wpv = fields.Monetary("Work Planned Value  Accourding to BOQ", currency_field="current_wpv_currency_id")
    current_wpv_currency_id = fields.Many2one('res.currency')
    previous_wpv = fields.Monetary("Previous Work Planned Value  Accourding to BOQ", currency_field="previous_wpv_currency_id")
    previous_wpv_currency_id = fields.Many2one('res.currency')
    current_wvcm = fields.Float("Work Value Completed This Month", compute="calc_current_wvcm")
    current_wvpm = fields.Float("Work Value Planned This Month",compute="calc_current_wvpm")
    current_wppp = fields.Float("Work Project Planned Progress This Month", compute="calc_current_wpppm")

    current_ppp = fields.Float("Project Planned Progress")
    # previous_ppp = fields.Float("Previous Project Planned Progress")
    current_pppp = fields.Float("Previous Project Planned Progress")
    # previous_pcp = fields.Float("Previous Project actual progress")
    current_pacp = fields.Float("Project Actual Progress")
    current_ppacp = fields.Float("Previous Project Actual Progress")
    current_wpacp = fields.Float("Work Project Actual Progress This Month", compute="calc_current_wpapm")

    ppptp = fields.Float("Project Planned Progress This Period")
    pcptp = fields.Float("Project Actual Progress This Period")
    oc_date = fields.Date("Original completion date")
    ec_date = fields.Date("Expected completion date")
    eoc_variance = fields.Float("Variance", compute="calc_eoc_variance")
    date_variance = fields.Float("Variance", compute="calc_eoc_variance")

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


    @api.onchange('project_end_date', 'project_start_date')
    @api.depends('project_end_date', 'project_start_date')
    def calc_elapsed_remaiing_time(self):
        for record in self:
            record.elapsed_time = 0.0
            record.remaining_time = 0.0
            if record.project_start_date and record.project_end_date:
                duration = (record.project_end_date - record.project_start_date).days
                elapsed_time = 0.0
                remaining_time = 0.0
                if datetime.now().date() > record.project_start_date:
                    elapsed_time = (datetime.now().date() - record.project_start_date).days
                if record.project_end_date > datetime.now().date():
                    remaining_time = (record.project_end_date - datetime.now().date()).days
                record.remaining_time = remaining_time / duration
                record.elapsed_time = elapsed_time / duration

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
    # document_submittal_log_details_ids totals
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

    def calc_acion_code(self):
        for record in self:
            record.h_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.dos == 'latest')))
            record.superseded_dos = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.dos == 'superseded')))
            record.opened_dosStatus = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.dosStatus == 'opened')))
            record.closed_dosStatus = len(
                record.document_submittal_log_details_ids.filtered((lambda line: line.dosStatus == 'closed')))
    #document_submittal_sd_log_details_ids totals
    h_co_action_code1 = fields.Integer('Under Approval', compute="calc_acion_code1")
    a_co_action_code1 = fields.Integer('Approval', compute="calc_acion_code1")
    b_co_action_code1 = fields.Integer('Approved With Comments', compute="calc_acion_code1")
    c_co_action_code1 = fields.Integer('Revise And Resubmit', compute="calc_acion_code1")
    d_co_action_code1 = fields.Integer('Rejected', compute="calc_acion_code1")
    cancel_co_action_code1 = fields.Integer('Cancelled', compute="calc_acion_code1")
    revision_co_action_code1 = fields.Integer('Revision', compute="calc_acion_code1")

    latest_dos1 = fields.Integer('Latest Documents', compute="calc_acion_code1")
    superseded_dos1 = fields.Integer('Superseded Documents', compute="calc_acion_code1")
    opened_dosStatus1 = fields.Integer('Opened Documents', compute="calc_acion_code1")
    closed_dosStatus1 = fields.Integer('Closed Documents', compute="calc_acion_code1")

    def calc_acion_code1(self):
        for record in self:
            record.h_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.dos == 'latest')))
            record.superseded_dos1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.dos == 'superseded')))
            record.opened_dosStatus1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.dosStatus == 'opened')))
            record.closed_dosStatus1 = len(
                record.document_submittal_sd_log_details_ids.filtered((lambda line: line.dosStatus == 'closed')))

    h_co_action_code2 = fields.Integer('Under Approval', compute="calc_acion_code2")
    a_co_action_code2 = fields.Integer('Approval', compute="calc_acion_code2")
    b_co_action_code2 = fields.Integer('Approved With Comments', compute="calc_acion_code2")
    c_co_action_code2 = fields.Integer('Revise And Resubmit', compute="calc_acion_code2")
    d_co_action_code2 = fields.Integer('Rejected', compute="calc_acion_code2")
    cancel_co_action_code2 = fields.Integer('Cancelled', compute="calc_acion_code2")
    revision_co_action_code2 = fields.Integer('Revision', compute="calc_acion_code2")

    latest_dos2 = fields.Integer('Latest Documents', compute="calc_acion_code2")
    superseded_dos2 = fields.Integer('Superseded Documents', compute="calc_acion_code2")
    opened_dosStatus2 = fields.Integer('Opened Documents', compute="calc_acion_code2")
    closed_dosStatus2 = fields.Integer('Closed Documents', compute="calc_acion_code2")

    def calc_acion_code2(self):
        for record in self:
            record.h_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.ir_latest_super == 'latest')))
            record.superseded_dos2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.ir_latest_super == 'superseded')))
            record.opened_dosStatus2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.irStatus == 'opened')))
            record.closed_dosStatus2 = len(
                record.inspection_request_log_details_ids.filtered((lambda line: line.irStatus == 'closed')))

    h_co_action_code3 = fields.Integer('Under Approval', compute="calc_acion_code3")
    a_co_action_code3 = fields.Integer('Approval', compute="calc_acion_code3")
    b_co_action_code3 = fields.Integer('Approved With Comments', compute="calc_acion_code3")
    c_co_action_code3 = fields.Integer('Revise And Resubmit', compute="calc_acion_code3")
    d_co_action_code3 = fields.Integer('Rejected', compute="calc_acion_code3")
    cancel_co_action_code3 = fields.Integer('Cancelled', compute="calc_acion_code3")
    revision_co_action_code3 = fields.Integer('Revision', compute="calc_acion_code3")

    latest_dos3 = fields.Integer('Latest Documents', compute="calc_acion_code3")
    superseded_dos3 = fields.Integer('Superseded Documents', compute="calc_acion_code3")
    opened_dosStatus3 = fields.Integer('Opened Documents', compute="calc_acion_code3")
    closed_dosStatus3 = fields.Integer('Closed Documents', compute="calc_acion_code3")

    def calc_acion_code3(self):
        for record in self:
            record.h_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered(
                    (lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code3 = len(
                record.material_inspection_request_log_details_ids.filtered(
                    (lambda line: line.action_code == 'revision')))

            record.latest_dos3 = len(
                record.material_inspection_request_log_details_ids.filtered(
                    (lambda line: line.mir_latest_super == 'latest')))
            record.superseded_dos3 = len(
                record.material_inspection_request_log_details_ids.filtered(
                    (lambda line: line.mir_latest_super == 'superseded')))
            record.opened_dosStatus3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.mirStatus == 'opened')))
            record.closed_dosStatus3 = len(
                record.material_inspection_request_log_details_ids.filtered((lambda line: line.mirStatus == 'closed')))

    h_co_action_code4 = fields.Integer('Under Approval', compute="calc_acion_code4")
    a_co_action_code4 = fields.Integer('Approval', compute="calc_acion_code4")
    b_co_action_code4 = fields.Integer('Approved With Comments', compute="calc_acion_code4")
    c_co_action_code4 = fields.Integer('Revise And Resubmit', compute="calc_acion_code4")
    d_co_action_code4 = fields.Integer('Rejected', compute="calc_acion_code4")
    cancel_co_action_code4 = fields.Integer('Cancelled', compute="calc_acion_code4")
    revision_co_action_code4 = fields.Integer('Revision', compute="calc_acion_code4")

    latest_dos4 = fields.Integer('Latest Documents', compute="calc_acion_code4")
    superseded_dos4 = fields.Integer('Superseded Documents', compute="calc_acion_code4")
    opened_dosStatus4 = fields.Integer('Opened Documents', compute="calc_acion_code4")
    closed_dosStatus4 = fields.Integer('Closed Documents', compute="calc_acion_code4")

    def calc_acion_code4(self):
        for record in self:
            record.h_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.mir_latest_super == 'latest')))
            record.superseded_dos4 = len(
                record.material_submittal_log_details_ids.filtered(
                    (lambda line: line.mir_latest_super == 'superseded')))
            record.opened_dosStatus4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.mirStatus == 'opened')))
            record.closed_dosStatus4 = len(
                record.material_submittal_log_details_ids.filtered((lambda line: line.mirStatus == 'closed')))

    h_co_action_code5 = fields.Integer('Under Approval', compute="calc_acion_code5")
    a_co_action_code5 = fields.Integer('Approval', compute="calc_acion_code5")
    b_co_action_code5 = fields.Integer('Approved With Comments', compute="calc_acion_code5")
    c_co_action_code5 = fields.Integer('Revise And Resubmit', compute="calc_acion_code5")
    d_co_action_code5 = fields.Integer('Rejected', compute="calc_acion_code5")
    cancel_co_action_code5 = fields.Integer('Cancelled', compute="calc_acion_code5")
    revision_co_action_code5 = fields.Integer('Revision', compute="calc_acion_code5")

    latest_dos5 = fields.Integer('Latest Documents', compute="calc_acion_code5")
    superseded_dos5 = fields.Integer('Superseded Documents', compute="calc_acion_code5")
    opened_dosStatus5 = fields.Integer('Opened Documents', compute="calc_acion_code5")
    closed_dosStatus5 = fields.Integer('Closed Documents', compute="calc_acion_code5")

    def calc_acion_code5(self):
        for record in self:
            record.h_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos5 = len(
                record.non_conformance_report_log_details_ids.filtered(
                    (lambda line: line.ncr_latest_super == 'latest')))
            record.superseded_dos5 = len(
                record.non_conformance_report_log_details_ids.filtered(
                    (lambda line: line.ncr_latest_super == 'superseded')))
            record.opened_dosStatus5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.ncrStatus == 'opened')))
            record.closed_dosStatus5 = len(
                record.non_conformance_report_log_details_ids.filtered((lambda line: line.ncrStatus == 'closed')))

    h_co_action_code6 = fields.Integer('Under Approval', compute="calc_acion_code6")
    a_co_action_code6 = fields.Integer('Approval', compute="calc_acion_code6")
    b_co_action_code6 = fields.Integer('Approved With Comments', compute="calc_acion_code6")
    c_co_action_code6 = fields.Integer('Revise And Resubmit', compute="calc_acion_code6")
    d_co_action_code6 = fields.Integer('Rejected', compute="calc_acion_code6")
    cancel_co_action_code6 = fields.Integer('Cancelled', compute="calc_acion_code6")
    revision_co_action_code6 = fields.Integer('Revision', compute="calc_acion_code6")

    latest_dos6 = fields.Integer('Latest Documents', compute="calc_acion_code6")
    superseded_dos6 = fields.Integer('Superseded Documents', compute="calc_acion_code6")
    opened_dosStatus6 = fields.Integer('Opened Documents', compute="calc_acion_code6")
    closed_dosStatus6 = fields.Integer('Closed Documents', compute="calc_acion_code6")

    def calc_acion_code6(self):
        for record in self:
            record.h_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'h')))
            record.a_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'a')))
            record.b_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'b')))
            record.c_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'c')))
            record.d_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'd')))
            record.cancel_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'cancelled')))
            record.revision_co_action_code6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.action_code == 'revision')))

            record.latest_dos6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfi_latest_super == 'latest')))
            record.superseded_dos6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfi_latest_super == 'superseded')))
            record.opened_dosStatus6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfiStatus == 'opened')))
            record.closed_dosStatus6 = len(
                record.request_for_information_log_details_ids.filtered((lambda line: line.rfiStatus == 'closed')))


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('document.submittal.log') or ' '
        return super(document_submittal_log, self).create(vals)

    def write(self, vals):
        vals['last_update'] = fields.Datetime.now()
        return super(document_submittal_log, self).write(vals)

    @api.onchange('project_id')
    def onchange_project_id(self):
        for record in self:
            if record.project_id:
                record.project_start_date = record.project_id.date_start
                record.project_end_date = record.project_id.date
                # record.project_code = record.project_id.date

    def open_simple_project_dashboard_action(self):
        action = self.env['ir.actions.act_window']._for_xml_id('diar_project_dashboard.open_simple_project_dashboard_action')
        action['name'] = _('Project Dashboard %s') % (self.name)
        action['res_id'] = self.id
        return action

    def action_print_dashboard_done(self):

        workbook = xlsxwriter.Workbook("charttttttttttt_pie.xlsx")

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({"bold": 1})

        # Add the worksheet data that the charts will refer to.
        headings = ["Category", "Values"]
        data = [
            ["Apple", "Cherry", "Pecan"],
            [60, 30, 10],
        ]

        worksheet.write_row("A1", headings, bold)
        worksheet.write_column("A2", data[0])
        worksheet.write_column("B2", data[1])

        #######################################################################
        #
        # Create a new chart object.
        #
        chart1 = workbook.add_chart({"type": "pie"})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart1.add_series(
            {
                "name": "Pie sales data",
                "categories": ["Sheet1", 1, 0, 3, 0],
                "values": ["Sheet1", 1, 1, 3, 1],
            }
        )

        # Add a title.
        chart1.set_title({"name": "Popular Pie Types"})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart1.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("C2", chart1, {"x_offset": 25, "y_offset": 10})
        workbook.close()
        # return True

    def action_print_dashboard1(self):
        workbook = xlsxwriter.Workbook("charttttttttttt_pie.xlsx")

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({"bold": 1})

        # Add the worksheet data that the charts will refer to.
        headings = ["Category", "Values"]
        data = [
            ['Elapsed Time', 'Remaining Time'],
            [self.elapsed_time * 100, self.remaining_time * 100],
        ]

        worksheet.write_row("F4", headings, bold)
        worksheet.write_column("F5", data[0])
        worksheet.write_column("G5", data[1])

        #######################################################################
        #
        # Create a new chart object.
        #
        chart1 = workbook.add_chart({"type": "pie"})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart1.add_series(
            {
                "name": "Pie sales data",
                "categories": ["Sheet1", 4, 5, 5, 6],
                "values": ["Sheet1", 4, 6, 5, 6],
                "data_labels": {'position': 'outside_end', 'percentage': True}
            }
        )

        # Add a title.
        chart1.set_title({"name": "Popular Pie Types"})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart1.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("F7", chart1, {"x_offset": 25, "y_offset": 10})
        workbook.close()
        # return True
    def get_excel_diar_projectdashboard_report(self):
        datas = {
            'ids': self,
            'model': 'document.submittal.log',
        }

        return self.env.ref('diar_project_dashboard.action_diar_project_dashboard_report_xlsx').report_action(self, data=datas)

    def action_print_dashboard(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        header1_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'font_size': 15, 'align': 'center', 'valign': 'vcenter', })
        workbook.add_format()
        add_format_emp1 = workbook.add_format(
            {'font_color': 'white', 'bold': 1, 'border': 1, 'font_size': 10, 'align': 'center',
             'valign': 'vcenter', 'fg_color': '#5f5e97', 'text_wrap': 'break-word', })
        add_format_emp_empty = workbook.add_format(
            {'fg_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, })
        add_format_emp = workbook.add_format({'fg_color': '#60C5E3', })
        worksheet = workbook.add_worksheet()
        worksheet.merge_range(0, 9, 0, 10, 'Printing Date', add_format_emp1)
        format5 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
        worksheet.merge_range(0, 11, 0, 12, datetime.now(), format5)
        worksheet.merge_range(1, 0, 1, 12,
                              str(self.project_id.name) + " - From : " + str(self.project_start_date) + " - " + str(
                                  self.project_end_date),
                              header1_format)
        worksheet.set_row(0, 20)
        worksheet.set_row(1, 40)
        worksheet.set_row(3, 25)
        worksheet.set_row(4, 25)
        worksheet.set_row(5, 25)
        worksheet.set_row(6, 25)
        worksheet.set_row(7, 25)
        worksheet.set_row(8, 25)
        worksheet.set_row(9, 25)
        worksheet.set_row(10, 25)
        worksheet.set_row(11, 25)
        worksheet.set_row(12, 25)
        worksheet.set_row(13, 25)
        worksheet.set_row(14, 25)
        worksheet.set_row(15, 25)
        worksheet.set_row(16, 25)
        worksheet.set_row(17, 25)
        worksheet.set_row(18, 25)
        worksheet.set_row(19, 25)

        worksheet.set_column(0, 75)
        row_2 = 3
        worksheet.merge_range(row_2, 0, row_2, 4, 'Contractual Data', add_format_emp1)
        row_2 = 4
        worksheet.merge_range(row_2, 0, row_2, 1, 'Project', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.project_id.name), add_format_emp_empty)
        row_2 = 5
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Contract Type', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.contract_type_id.name), add_format_emp_empty)
        row_2 = 6
        worksheet.merge_range(row_2, 0, row_2, 1, 'Owner', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.project_id.partner_id.name or ''), add_format_emp_empty)

        row_2 = 7
        worksheet.merge_range(row_2, 0, row_2, 1, 'Number of Hospital Beds', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.NumberofHospitalBeds), add_format_emp_empty)

        row_2 = 8
        worksheet.merge_range(row_2, 0, row_2, 1, 'Number of Floors', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.NumberofFloors), add_format_emp_empty)

        row_2 = 9
        worksheet.merge_range(row_2, 0, row_2, 1, 'Total Project Area (m2)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.TotalProjectArea_m2), add_format_emp_empty)

        row_2 = 10
        worksheet.merge_range(row_2, 0, row_2, 1, 'Project Budget (EGP)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.Project_Budget), add_format_emp_empty)
        row_2 = 11
        worksheet.merge_range(row_2, 0, row_2, 1, 'Advance Payment (EGP)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.Advance_Payment), add_format_emp_empty)
        row_2 = 12
        worksheet.merge_range(row_2, 0, row_2, 1, 'Retention', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.Retention), add_format_emp_empty)
        row_2 = 13
        worksheet.merge_range(row_2, 0, row_2, 1, 'Commencement Date', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(self.Commencement_Date), add_format_emp_empty)
        row_2 = 14
        worksheet.merge_range(row_2, 0, row_2, 1, 'Project Duration (Days)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, (self.project_end_date - self.project_start_date).days,
                              add_format_emp_empty)
        row_2 = 15
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Consultant', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, self.main_consultant_res_partner_id.name, add_format_emp_empty)
        row_2 = 16
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Contractor', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, self.main_contractor_res_partner_id.name, add_format_emp_empty)
        row_2 = 17
        worksheet.merge_range(row_2, 0, row_2, 1, "The contractor's consultant", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, self.consultant_res_partner_id.name, add_format_emp_empty)
        row_2 = 18
        worksheet.merge_range(row_2, 0, row_2, 1, "The Sub Contractor", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, self.contractor_res_partner_id.name, add_format_emp_empty)
        row_2 = 19
        worksheet.merge_range(row_2, 0, row_2, 1, "The Sub contractor's consultant", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, self.consultant_res_partner_id.name, add_format_emp_empty)

        bold = workbook.add_format({"bold": 1})

        # Add the worksheet data that the charts will refer to.
        headings = ["Category", "Values"]
        data = [
            ['Elapsed Time', 'Remaining Time'],
            [round(self.elapsed_time * 100), round(self.remaining_time * 100)],
        ]

        # worksheet.write_row("F4", headings, bold)
        worksheet.write_column("F5", data[0], bold)
        worksheet.write_column("G5", data[1])

        #######################################################################
        #
        # Create a new chart object.
        #
        chart1 = workbook.add_chart({"type": "doughnut"})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart1.add_series(
            {
                "name": "Pie sales data",
                "categories": ["Sheet1", 4, 5, 5, 6],
                "values": ["Sheet1", 4, 6, 5, 6],
                "data_labels": {'position': 'outside_end', 'percentage': True}
            }
        )
        # Add a title.
        remaining_time = (self.project_end_date - datetime.now().date()).days
        chart1.set_title({"name": "Project Duration(Days): " + str(remaining_time) +"\n Effective Variance(Days):"+ str(int(self.date_variance))})
        # Set an Excel chart style. Colors with white outline and shadow.
        chart1.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("F4", chart1, {"x_offset": 0.5, "y_offset": 0})

        #######################################################################
        #
        # Create a new chart object.
        #
        data2 = [
            ['Product Budget', 'Advanced Payment', 'Remaining Payment'],
            [self.Project_Budget, self.Advance_Payment, self.Project_Budget-self.Advance_Payment],
        ]

        # worksheet.write_row("F4", headings, bold)
        worksheet.write_column("F7", data2[0], bold)
        worksheet.write_column("G7", data2[1])
        chart2 = workbook.add_chart({"type": "doughnut"})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart2.add_series(
            {
                "name": "Project Budget Data",
                "categories": ["Sheet1", 6, 5, 8, 5],
                "values": ["Sheet1", 6, 7, 8, 5],
                "data_labels": {'position': 'outside_end', 'percentage': True}
            }
        )
        # Add a title.
        remaining_time = (self.project_end_date - datetime.now().date()).days
        chart2.set_title({"name": "Project Payment" })
        # Set an Excel chart style. Colors with white outline and shadow.
        chart2.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("F13", chart2, {"x_offset": 0, "y_offset": 0})
        #########Column Chart########################
        data = [["% Project Planned Progress", "% Project Actual Progress", "% Work Project Planned Progress This Month", "% Work Project Actual Progress This Month"],
                [self.current_ppp, self.current_pacp, self.current_wppp, self.current_wpacp]]
        worksheet.write_column("A34", data[0])
        worksheet.write_column("B34", data[1])
        column_chart1 = workbook.add_chart({"type": "column"})
        column_chart1.add_series(
            {
                "categories": ["Sheet1", 32, 0, 36, 0],
                "values": ["Sheet1", 32, 1, 36, 1],
                'line': {'color': 'blue'},
                'overlap': 10,
            }
        )
        column_chart1.set_title({"name": " Project % Complete "})
        column_chart1.set_y_axis({"name": "Totals", "major_units": 0.25, "num_format": "0"})
        column_chart1.set_style(20)
        worksheet.insert_chart("N4", column_chart1, {"x_offset": 0, "y_offset": 0})
        #########Column Chart########################
        data = [["Work Value Planned This Month", "Work Value Completed This Month","Work Completed Value Accourding to BOQ", "Work Planned Value Accourding to BOQ", "Total Budget"],
                [self.current_wvpm ,self.current_wvcm,self.current_wcv, self.current_wpv, self.Project_Budget]]
        worksheet.write_column("A39", data[0])
        worksheet.write_column("B39", data[1])
        column_chart1 = workbook.add_chart({"type": "column"})
        column_chart1.add_series(
            {
                "categories": ["Sheet1", 37, 0, 40, 0],
                "values": ["Sheet1", 37, 1, 40, 1],
                'line': {'color': 'blue'},
                'overlap': 10,
            }
        )
        column_chart1.set_title({"name": " Project Budget "})
        column_chart1.set_y_axis({"name": "Totals", "major_units": 0.25, "num_format": "0"})
        column_chart1.set_style(20)
        worksheet.insert_chart("N13", column_chart1, {"x_offset": 0, "y_offset": 0})
        #########Column Chart########################
        # data = [
        #     ["Under Approval", "Approval", "Approved With Comments", "Revise And Resubmit", "Rejected", "Cancelled","Revision", "Latest Documents", "Superseded Documents", "Opened Documents", "Closed Documents"],
        #     [self.h_co_action_code1, self.a_co_action_code1, self.b_co_action_code1, self.c_co_action_code1,self.d_co_action_code1, self.cancel_co_action_code1, self.revision_co_action_code1, self.latest_dos1,self.superseded_dos1, self.opened_dosStatus1, self.closed_dosStatus1],
        #     ]
        # worksheet.write_column("A22", data[0])
        # worksheet.write_column("B22", data[1])
        # column_chart1.add_series(
        #     {
        #         "name": "Document Submittal SD Logs",
        #         "categories": ["Sheet1", 21, 0, 33, 0],
        #         "values": ["Sheet1", 21, 1, 33, 1],
        #         'line': {'color': 'red'},
        #         'overlap': 10,
        #     }
        # )
        # column_chart1.set_title({"name": " Totals "})
        # # column_chart1.set_x_axis({"name": "Submitted For"})
        # column_chart1.set_y_axis({"name": "Totals", "major_units": 0.25, "num_format": "0"})
        #
        # # Set an Excel chart style.
        # column_chart1.set_style(20)
        #
        # # Insert the chart into the worksheet (with an offset).
        # worksheet.insert_chart("A25", column_chart1, {"x_offset": 0, "y_offset": 0, 'x_scale': 2.25, 'y_scale': 1.75})

        # #########Column Chart########################
        data = [
            ["Under Approval", "Approval", "Approved With Comments", "Revise And Resubmit", "Rejected", "Cancelled", "Revision", "Latest Documents","Superseded Documents","Opened Documents","Closed Documents"],
            [self.h_co_action_code, self.a_co_action_code, self.b_co_action_code, self.c_co_action_code, self.d_co_action_code, self.cancel_co_action_code, self.revision_co_action_code, self.latest_dos, self.superseded_dos, self.opened_dosStatus, self.closed_dosStatus],
            [self.h_co_action_code1, self.a_co_action_code1, self.b_co_action_code1, self.c_co_action_code1, self.d_co_action_code1, self.cancel_co_action_code1, self.revision_co_action_code1, self.latest_dos1, self.superseded_dos1, self.opened_dosStatus1, self.closed_dosStatus1],
            [self.h_co_action_code2, self.a_co_action_code2, self.b_co_action_code2, self.c_co_action_code2, self.d_co_action_code2, self.cancel_co_action_code2, self.revision_co_action_code2, self.latest_dos2, self.superseded_dos2, self.opened_dosStatus2, self.closed_dosStatus2],
            [self.h_co_action_code3, self.a_co_action_code3, self.b_co_action_code3, self.c_co_action_code3, self.d_co_action_code3, self.cancel_co_action_code3, self.revision_co_action_code3, self.latest_dos3, self.superseded_dos3, self.opened_dosStatus3, self.closed_dosStatus3],
            [self.h_co_action_code4, self.a_co_action_code4, self.b_co_action_code4, self.c_co_action_code4, self.d_co_action_code4, self.cancel_co_action_code4, self.revision_co_action_code4, self.latest_dos4, self.superseded_dos4, self.opened_dosStatus4, self.closed_dosStatus4],
            [self.h_co_action_code5, self.a_co_action_code5, self.b_co_action_code5, self.c_co_action_code5, self.d_co_action_code5, self.cancel_co_action_code5, self.revision_co_action_code5, self.latest_dos5, self.superseded_dos5, self.opened_dosStatus5, self.closed_dosStatus5],
            [self.h_co_action_code6, self.a_co_action_code6, self.b_co_action_code6, self.c_co_action_code6, self.d_co_action_code6, self.cancel_co_action_code6, self.revision_co_action_code6, self.latest_dos6, self.superseded_dos6, self.opened_dosStatus6, self.closed_dosStatus6],
        ]
        worksheet.write_column("A22", data[0])
        worksheet.write_column("B22", data[1])
        worksheet.write_column("C22", data[2])
        worksheet.write_column("D22", data[3])
        worksheet.write_column("E22", data[4])
        worksheet.write_column("F22", data[5])
        worksheet.write_column("G22", data[6])
        worksheet.write_column("H22", data[7])
        column_chart1 = workbook.add_chart({"type": "column"})
        # column_chart1.add_series({"values": "=Sheet1!$A$22:$A$32"})
        column_chart1.add_series(
            {
                # "name": 'Document Submittal Logs',
                "categories": ["Sheet1", 21, 0, 31, 0],
                "values": ["Sheet1", 21, 1, 31, 1],
                'line': {'color': 'blue'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Document Submittal SD Logs",
                "categories": ["Sheet1", 21, 1, 31, 1],
                "values": ["Sheet1", 21, 2, 31, 2],
                'line': {'color': 'red'},
                'overlap': 10,
            }
        )
        # column_chart1.add_series(
        #     {
        #         "name": "Inspection Request Logs",
        #         "categories": ["Sheet1", 21, 2, 31, 2],
        #         "values": ["Sheet1", 21, 3, 31, 3],
        #         'line': {'color': 'green'},
        #         'overlap': 10,
        #     }
        # )
        # column_chart1.add_series(
        #     {
        #         "name": "Material Inspection Request Logs",
        #         "categories": ["Sheet1", 21, 3, 31, 3],
        #         "values": ["Sheet1", 21, 4, 31, 4],
        #         'line': {'color': 'green'},
        #         'overlap': 10,
        #     }
        # )
        column_chart1.add_series(
            {
                "name": "Material Submittal Logs",
                "categories": ["Sheet1", 21, 4, 31, 4],
                "values": ["Sheet1", 21, 5, 31, 5],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        # column_chart1.add_series(
        #     {
        #         "name": "Non Conformance Report Logs",
        #         "categories": ["Sheet1", 21, 5, 31, 5],
        #         "values": ["Sheet1", 21, 6, 31, 6],
        #         'line': {'color': 'green'},
        #         'overlap': 10,
        #     }
        # )
        # column_chart1.add_series(
        #     {
        #         "name": "Request For Information Logs",
        #         "categories": ["Sheet1", 21, 6, 31, 6],
        #         "values": ["Sheet1", 21, 7, 31, 7],
        #         'line': {'color': 'green'},
        #         'overlap': 10,
        #     }
        # )
        column_chart1.set_title({"name": " Totals "})
        # column_chart1.set_x_axis({"name": "Submitted For"})
        column_chart1.set_y_axis({"name": "Totals","major_units": 0.25, "num_format": "0"})

        # Set an Excel chart style.
        column_chart1.set_style(20)

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("A22", column_chart1, {"x_offset": 0, "y_offset": 0,'x_scale': 2.25, 'y_scale': 1.75})

        if self.env.user.lang == 'ar_SY':
            worksheet.right_to_left()
        workbook.close()
        output.seek(0)
        return self.env['binary.downloads'].get_download_url({
            'filename': 'Document Submittal Log:' + str(self.project_start_date) + "-" + str(
                self.project_end_date) + ".xlsx",
            'content': base64.encodebytes(output.read()),  #decodebytes
        })

    def action_import_submittal_log_details_file(self):
        self.document_submittal_log_details_ids.unlink()
        if not self.submittal_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.submittal_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'submittal log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                from_res_partner_obj = self.env['res.partner'].search([('name', '=', line[2])], limit=1)
                from_res_partner_id = from_res_partner_obj.id or ''
                to_res_partner_obj = self.env['res.partner'].search([('name', '=', line[3])], limit=1)
                to_res_partner_id = to_res_partner_obj.id or ''
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[4])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[19])], limit=1)
                res_country_id = res_country_obj.id or ''
                sentdate = datetime.utcfromtimestamp((float(line[9]) - 25569) * 86400.0)
                duedate = datetime.utcfromtimestamp((float(line[10]) - 25569) * 86400.0)
                receiveddate = datetime.utcfromtimestamp((float(line[11]) - 25569) * 86400.0)
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'discipline_section_id': discipline_section_id,
                    'submittal_Type': line[5],
                    'name': line[6],
                    'copy_type': str(line[8]).lower(),
                    'sentdate': sentdate,
                    'duedate': duedate,
                    'receiveddate': receiveddate,
                    'action_code': str(line[14]).lower(),
                    'dos': str(line[15]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[20],
                    'scope': line[21],
                    'notes': line[22],
                })
                self.document_submittal_log_details_ids = [(0, 0, data_list)]

    def action_import_submittal_sd_log_details_file(self):
        self.document_submittal_sd_log_details_ids.unlink()
        if not self.submittal_sd_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.submittal_sd_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'submittal sd log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[6])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[22])], limit=1)
                res_country_id = res_country_obj.id or ''
                sentdate = datetime.utcfromtimestamp((float(line[12]) - 25569) * 86400.0)
                duedate = datetime.utcfromtimestamp((float(line[13]) - 25569) * 86400.0)
                receiveddate = datetime.utcfromtimestamp((float(line[14]) - 25569) * 86400.0)
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'drawing_number': line[4] or '',
                    'drawing_rev': line[5] or '',
                    'discipline_section_id': discipline_section_id,
                    'item_name': line[7] or '',
                    'Level': line[8] or '',
                    'drawing_title': line[9] or '',
                    'copy_type': str(line[11]).lower(),
                    'sentdate': sentdate,
                    'duedate': duedate,
                    'receiveddate': receiveddate,
                    'action_code': str(line[17]).lower(),
                    'dos': str(line[18]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[23],
                    'scope': line[24],
                    'notes': line[25],
                })
                self.document_submittal_sd_log_details_ids = [(0, 0, data_list)]

    def action_import_inspection_request_log_details_file(self):
        self.inspection_request_log_details_ids.unlink()
        if not self.inspection_request_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.inspection_request_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'submittal log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[4])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[22])], limit=1)
                res_country_id = res_country_obj.id or ''
                sentdate = datetime.utcfromtimestamp((float(line[11]) - 25569) * 86400.0)
                inspection_date = datetime.utcfromtimestamp((float(line[12]) - 25569) * 86400.0)
                duedate = datetime.utcfromtimestamp((float(line[13]) - 25569) * 86400.0)
                receiveddate = datetime.utcfromtimestamp((float(line[14]) - 25569) * 86400.0)
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'discipline_section_id': discipline_section_id,
                    'item_type':line[5] or '',
                    'item_name': line[6] or '',
                    'location_Level': line[7] or '',
                    'name': line[8],
                    'copy_type': str(line[10]).lower(),
                    'sentdate': sentdate,
                    'inspection_date':inspection_date,
                    'duedate': duedate,
                    'receiveddate': receiveddate,
                    'action_code': str(line[17]).lower(),
                    'ir_latest_super': str(line[18]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[23],
                    'scope': line[24],
                    'notes': line[25]
                })
                self.inspection_request_log_details_ids = [(0, 0, data_list)]

    def action_import_material_inspection_request_log_details_file(self):
        self.material_inspection_request_log_details_ids.unlink()
        if not self.material_inspection_request_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.material_inspection_request_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'submittal log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[4])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[20])], limit=1)
                res_country_id = res_country_obj.id or ''
                inspection_date = datetime.utcfromtimestamp((float(line[10]) - 25569) * 86400.0)
                duedate = datetime.utcfromtimestamp((float(line[11]) - 25569) * 86400.0)
                receiveddate = datetime.utcfromtimestamp((float(line[12]) - 25569) * 86400.0)
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'discipline_section_id': discipline_section_id,
                    'manufacture_name': line[6] or '',
                    'material_name': line[5] or '',
                    'name': line[7] or '',
                    'copy_type': str(line[9]).lower(),
                    'inspection_date': inspection_date,
                    'duedate': duedate,
                    'receiveddate': receiveddate,
                    'action_code': str(line[15]).lower(),
                    'mir_latest_super': str(line[16]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[21],
                    'scope': line[22],
                    'notes': line[23]
                })
                self.material_inspection_request_log_details_ids = [(0, 0, data_list)]

    def action_import_material_submittal_log_details_file(self):
        self.material_submittal_log_details_ids.unlink()
        if not self.material_submittal_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.material_submittal_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'material submittal log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[4])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[21])], limit=1)
                res_country_id = res_country_obj.id or ''
                sentdate = (datetime.utcfromtimestamp((float(line[11]) - 25569) * 86400.0)) if line[11] else ''
                duedate = (datetime.utcfromtimestamp((float(line[12]) - 25569) * 86400.0)) if line[12] else ''
                receiveddate = (datetime.utcfromtimestamp((float(line[13]) - 25569) * 86400.0)) if line[13] else ''
                if str(line[9]).lower() == 'not attached':
                    material_sample = 'notattached'
                elif str(line[9]).lower() == 'attached':
                    material_sample = 'attached'
                else:
                    material_sample = ''
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'discipline_section_id': discipline_section_id,
                    'manufacture_name': line[6] or '',
                    'material_name': line[5] or '',
                    'name': line[7] or '',
                    'material_sample': material_sample,
                    'copy_type': str(line[10]).lower(),

                    'sentdate': sentdate,
                    'duedate': duedate,
                    'receiveddate': receiveddate,

                    'action_code': str(line[16]).lower(),
                    'mir_latest_super': str(line[17]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[22],
                    'scope': line[23],
                    'notes': line[24]
                })
                self.material_submittal_log_details_ids = [(0, 0, data_list)]

    def action_import_request_for_information_log_details_file(self):
        self.request_for_information_log_details_ids.unlink()
        if not self.request_for_information_log_details_file:
            raise ValidationError(_("Sorry you must select the file"))
        try:
            wb = open_workbook(file_contents=base64.decodebytes(self.request_for_information_log_details_file))
        except Exception as e:
            raise ValidationError(_("Sorry Error while reading 'material submittal log details file' file"))
        sheet = wb.sheet_by_index(0)
        data_list = {}
        for row_no in range(9, sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                discipline_section_obj = self.env['discipline.section'].search([('code', '=', line[4])], limit=1)
                discipline_section_id = discipline_section_obj.id or ''
                res_country_obj = self.env['res.country'].search([('name', '=', line[21])], limit=1)
                res_country_id = res_country_obj.id or ''
                sentdate = (datetime.utcfromtimestamp((float(line[11]) - 25569) * 86400.0)) if line[11] else ''
                duedate = (datetime.utcfromtimestamp((float(line[12]) - 25569) * 86400.0)) if line[12] else ''
                receiveddate = (datetime.utcfromtimestamp((float(line[13]) - 25569) * 86400.0)) if line[13] else ''
                if str(line[9]).lower() == 'not attached':
                    material_sample = 'notattached'
                elif str(line[9]).lower() == 'attached':
                    material_sample = 'attached'
                else:
                    material_sample = ''
                data_list.update({
                    'reference': line[0] or '',
                    'review': line[1] or '',
                    'discipline_section_id': discipline_section_id,
                    'manufacture_name': line[6] or '',
                    'material_name': line[5] or '',
                    'name': line[7] or '',
                    'material_sample': material_sample,
                    'copy_type': str(line[10]).lower(),

                    'sentdate': sentdate,
                    'duedate': duedate,
                    'receiveddate': receiveddate,

                    'action_code': str(line[16]).lower(),
                    'mir_latest_super': str(line[17]).lower(),
                    'res_country_id': res_country_id,
                    'packageType': line[22],
                    'scope': line[23],
                    'notes': line[24]
                })
                self.request_for_information_log_details_ids = [(0, 0, data_list)]

class wizard_excel_report(models.Model):
    _name = "wizard.excel.report"
    excel_file = fields.Binary('excel file')
    file_name = fields.Char('Excel File', size=64)


class document_submittal_log_details(models.Model):
    _name = 'document.submittal.log.details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Document Submittal Log Details"

    document_submittal_log_id = fields.Many2one('document.submittal.log', 'Document Submittal Log')

    reference = fields.Char('Document Submittal Ref.', track_visibility='always')
    review = fields.Char('Submittal Rev..', track_visibility='always')
    from_res_partner_id = fields.Many2one('res.partner', related="document_submittal_log_id.from_res_partner_id", string='From The sender', store=True, readonly=False)
    to_res_partner_id = fields.Many2one('res.partner', related="document_submittal_log_id.to_res_partner_id", string='To The recipient', store=True, readonly=False)
    discipline_section_id = fields.Many2one('discipline.section', 'Discipline', track_visibility='always')
    submittal_Type = fields.Char('Submittal Type', track_visibility='always')
    name = fields.Char('Subject', track_visibility='always')
    copy_type = fields.Selection([('hard', 'Hard'), ('soft', 'Soft')], 'Copy Type', track_visibility='always')
    sentdate = fields.Date('Sent Date ', track_visibility='always')
    duedate = fields.Date('Due Date ', track_visibility='always')
    receiveddate = fields.Date('Received Date ', track_visibility='always')
    replyduration = fields.Integer('Reply Duration', compute="calc_replyduration", track_visibility='always')
    action_code = fields.Selection(
        [('h', 'H'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('cancelled', 'Cancelled'),
         ('revision', 'Revision')], 'Action Code', track_visibility='always')
    submittedfor = fields.Char('Submitted For', track_visibility='always',compute="onchange_action_code")
    dos = fields.Selection([('latest', 'Latest'), ('superseded', 'Superseded')], 'DOS (Latest-Superseded)',
                           track_visibility='always')
    dosStatus = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')], 'DOS Status(Opened-Closed)',
                                 track_visibility='always', compute="onchange_code_dos")
    native_file = fields.Binary('Native File', track_visibility='always')
    native_file_name = fields.Char('Native File', track_visibility='always')
    scan_file = fields.Binary('Scan File', track_visibility='always')
    scan_file_name = fields.Char('Scan File', track_visibility='always')
    res_country_id = fields.Many2one('res.country', 'Country', track_visibility='always')
    packageType = fields.Char('Package Type', track_visibility='always')
    scope = fields.Char('Scope', track_visibility='always')
    notes = fields.Text('Notes', track_visibility='always')

    @api.onchange('action_code')
    def onchange_code_dos1(self):
        for record in self:
            if record.action_code:
                record.receiveddate = datetime.now()
    @api.onchange('action_code', 'dos')
    @api.depends('action_code', 'dos')
    def onchange_code_dos(self):
        for record in self:
            if record.action_code == 'h':
                record.dosStatus = 'opened'
            elif record.action_code == 'c' and record.dos == 'latest':
                record.dosStatus = 'opened'
            else:
                record.dosStatus = 'closed'


    @api.onchange('action_code')
    @api.depends('action_code')
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
            else:
                record.submittedfor = ""

    @api.constrains()
    def check_dates(self):
        for record in self:
            if record.sentdate and record.receiveddate and record.receiveddate < record.sentdate:
                raise ValidationError(_("Sorry send date can't exceed received date"))

    @api.depends('sentdate', 'receiveddate')
    def calc_replyduration(self):
        for record in self:
            record.replyduration = 0
            if record.sentdate and record.receiveddate and record.receiveddate < record.sentdate:
                raise ValidationError(_("Sorry send date can't exceed received date"))
            if record.sentdate and record.receiveddate and record.receiveddate > record.sentdate:
                record.replyduration = (record.receiveddate - record.sentdate).days
