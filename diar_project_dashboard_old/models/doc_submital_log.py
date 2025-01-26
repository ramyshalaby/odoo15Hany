# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import io, base64, xlsxwriter, xlwt
from io import StringIO


class document_submittal_log(models.Model):
    _name = 'document.submittal.log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Document Submittal Log"

    name = fields.Char('Name', track_visibility='always')
    project_id = fields.Many2one('project.project', 'Project', track_visibility='always')
    partner_id = fields.Many2one('res.partner', related="project_id.partner_id", string='Project Customer(Owner)')
    contract_type_id = fields.Many2one('contract.type', 'Contract Type', track_visibility='always')

    Project_Budget = fields.Float("Project Budget (EGP)", track_visibility='always')
    Advance_Payment = fields.Float("Advance Payment (EGP)", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Advance_Payment_Per = fields.Float("Advance Payment %", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Retention_percentage = fields.Float("Retention % ", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)
    Retention = fields.Float("Retention", track_visibility='always', compute="calc_Advance_Payment", readonly=False, store=True)

    @api.depends('Project_Budget', 'Advance_Payment_Per','Advance_Payment')
    def calc_Advance_Payment(self):
        for record in self:
            record.Advance_Payment = record.Project_Budget * record.Advance_Payment_Per
            record.Advance_Payment_Per = record.Advance_Payment / record.Project_Budget
            record.Retention_percentage = record.Retention / record.Project_Budget
            record.Retention = record.Retention_percentage * record.Project_Budget

    @api.onchange('Project_Budget', 'Advance_Payment_Per')
    def onchange_Advance_Payment_Per(self):
        for record in self:
            if record.Project_Budget > 0 and record.Advance_Payment_Per > 0:
                record.Advance_Payment = record.Project_Budget * record.Advance_Payment_Per
    #
    @api.onchange('Project_Budget', 'Advance_Payment')
    def onchange_Advance_Payment_Per2(self):
        for record in self:
            if record.Advance_Payment > 0 and record.Project_Budget>0:
                record.Advance_Payment_Per = record.Advance_Payment / record.Project_Budget

    Retention_percentage = fields.Float("Retention % ", track_visibility='always')
    Retention = fields.Float("Retention", track_visibility='always', compute="calc_Retention")
    Commencement_Date = fields.Date("Commencement Date", track_visibility='always')
    Project_Duration = fields.Float("Project Duration (Days)", track_visibility='always')

    project_start_date = fields.Date('Start Date', track_visibility='always')
    project_end_date = fields.Date('End Date', track_visibility='always')
    elapsed_time = fields.Float("Elapsed Time %", compute="calc_elapsed_remaiing_time")
    remaining_time = fields.Float("Remaining Time %", compute="calc_elapsed_remaiing_time")
    project_code = fields.Char('Project Code', track_visibility='always')
    diar_scope = fields.Text('Diar Scope', track_visibility='always')
    main_contractor_res_partner_id = fields.Many2one('res.partner', 'Main Contractor', track_visibility='always')
    contractor_res_partner_id = fields.Many2one('res.partner', 'Contractor', track_visibility='always')
    main_consultant_res_partner_id = fields.Many2one('res.partner', 'Main Consultant', track_visibility='always')
    consultant_res_partner_id = fields.Many2one('res.partner', 'Consultant', track_visibility='always')
    last_update = fields.Datetime('Last Update', track_visibility='always')
    document_submittal_log_details_ids = fields.One2many('document.submittal.log.details', 'document_submittal_log_id',
                                                         'Document Submittal Logs')
    NumberofHospitalBeds = fields.Integer('Number of Hospital Beds', track_visibility='always')
    NumberofFloors = fields.Char("Number of Floors", track_visibility='always')
    TotalProjectArea_m2 = fields.Float("Total Project Area (m2)", track_visibility='always')

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

    @api.depends('Retention_percentage', 'Project_Budget')
    def calc_Retention(self):
        for record in self:
            record.Retention = 0.0
            if record.Project_Budget and record.Retention_percentage:
                record.Retention = record.Retention_percentage * record.Project_Budget

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
        chart1.set_title({"name": "Project Duration\nVariance (Days): " + str(remaining_time)})
        # Set an Excel chart style. Colors with white outline and shadow.
        chart1.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("F5", chart1, {"x_offset": 0, "y_offset": 0})
        #########Column Chart########################
        headings = ["Under Approval", "Approval", "Approved With Comments", "Revise And Resubmit", "Rejected", "Cancelled", "Revision"]
        data = [
            ["Under Approval", "Approval", "Approved With Comments", "Revise And Resubmit", "Rejected", "Cancelled", "Revision"],
            [self.h_co_action_code, self.a_co_action_code, self.b_co_action_code, self.c_co_action_code, self.d_co_action_code, self.cancel_co_action_code, self.revision_co_action_code]
        ]
        worksheet.write_column("A22", data[0])
        worksheet.write_column("B22", data[1])
        column_chart1 = workbook.add_chart({"type": "column"})
        column_chart1.add_series({"values": "=Sheet1!$A$22:$A$29"})
        column_chart1.add_series(
            {
                "name": ["Sheet1", 21, 27],
                "categories": ["Sheet1", 21, 0, 27, 0],
                "values": ["Sheet1", 21, 1, 27, 1],
            }
        )
        column_chart1.set_title({"name": " Materials Status"})
        column_chart1.set_x_axis({"name": "Submitted For"})
        column_chart1.set_y_axis({"name": "Total","major_units": 0.25, "num_format": "0"})

        # Set an Excel chart style.
        column_chart1.set_style(20)

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("A22", column_chart1, {"x_offset": 0, "y_offset": 0,'x_scale': 1, 'y_scale': 2})

        if self.env.user.lang == 'ar_SY':
            worksheet.right_to_left()
        workbook.close()
        output.seek(0)
        return self.env['binary.downloads'].get_download_url({
            'filename': 'Document Submittal Log:' + str(self.project_start_date) + "-" + str(
                self.project_end_date) + ".xlsx",
            'content': base64.encodebytes(output.read()),  #decodebytes
        })


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
    from_res_partner_id = fields.Many2one('res.partner', 'From The sender')
    to_res_partner_id = fields.Many2one('res.partner', 'To The recipient')
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
    submittedfor = fields.Char('Submitted For', track_visibility='always')
    dos = fields.Selection([('latest', 'Latest'), ('superseded', 'Superseded')], 'DOS (Latest-Superseded)',
                           track_visibility='always')
    dosStatus = fields.Selection([('opened', 'Opened'), ('closed', 'Closed')], 'DOS Status(Opened-Closed)',
                                 track_visibility='always')
    native_file = fields.Binary('Native File', track_visibility='always')
    native_file_name = fields.Char('Native File', track_visibility='always')
    scan_file = fields.Binary('Scan File', track_visibility='always')
    scan_file_name = fields.Char('Scan File', track_visibility='always')
    res_country_id = fields.Many2one('res.country', 'Country', track_visibility='always')
    packageType = fields.Char('Package Type', track_visibility='always')
    scope = fields.Char('Scope', track_visibility='always')
    notes = fields.Text('Notes', track_visibility='always')

    @api.onchange('action_code', 'dos')
    def onchange_code_dos(self):
        for record in self:
            if record.action_code == 'h':
                record.dosStatus = 'opened'
            elif record.action_code == 'c' and record.dos == 'latest':
                record.dosStatus = 'opened'
            else:
                record.dosStatus = 'closed'
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

    @api.depends('sentdate', 'receiveddate')
    def calc_replyduration(self):
        for record in self:
            record.replyduration = 0
            if record.sentdate and record.receiveddate and record.receiveddate < record.sentdate:
                raise ValidationError(_("Sorry send date can't exceed received date"))
            if record.sentdate and record.receiveddate and record.receiveddate > record.sentdate:
                record.replyduration = (record.receiveddate - record.sentdate).days
