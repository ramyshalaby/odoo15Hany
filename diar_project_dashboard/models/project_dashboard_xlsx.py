# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
import io
from xlsxwriter import workbook
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class project_dashboard_xlsx(models.AbstractModel):
    _name = 'report.diar_project_dashboard.report_project_dashboard_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, dashboard_obj):
        # output = io.BytesIO()
        # workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        worksheet = workbook.add_worksheet()
        header1_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'font_size': 15, 'align': 'center', 'valign': 'vcenter', })
        workbook.add_format()
        add_format_emp1 = workbook.add_format(
            {'font_color': 'white', 'bold': 1, 'border': 1, 'font_size': 10, 'align': 'center',
             'valign': 'vcenter', 'fg_color': '#5f5e97', 'text_wrap': 'break-word', })
        add_format_emp_empty = workbook.add_format(
            {'fg_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, })
        add_format_emp = workbook.add_format({'fg_color': '#60C5E3', })
        worksheet.merge_range(0, 9, 0, 10, 'Printing Date', add_format_emp1)
        format5 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
        worksheet.merge_range(0, 11, 0, 12, datetime.now(), format5)
        worksheet.merge_range(1, 0, 1, 12,
                              str(dashboard_obj.project_id.name) + " - From : " + str(dashboard_obj.project_start_date) + " - " + str(
                                  dashboard_obj.project_end_date),
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
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.project_id.name), add_format_emp_empty)
        row_2 = 5
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Contract Type', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.contract_type_id.name), add_format_emp_empty)
        row_2 = 6
        worksheet.merge_range(row_2, 0, row_2, 1, 'Owner', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.project_id.partner_id.name or ''), add_format_emp_empty)

        row_2 = 7
        worksheet.merge_range(row_2, 0, row_2, 1, 'Number of Hospital Beds', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.NumberofHospitalBeds), add_format_emp_empty)

        row_2 = 8
        worksheet.merge_range(row_2, 0, row_2, 1, 'Number of Floors', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.NumberofFloors), add_format_emp_empty)

        row_2 = 9
        worksheet.merge_range(row_2, 0, row_2, 1, 'Total Project Area (m2)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.TotalProjectArea_m2), add_format_emp_empty)

        row_2 = 10
        worksheet.merge_range(row_2, 0, row_2, 1, 'Project Budget (EGP)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.Project_Budget), add_format_emp_empty)
        row_2 = 11
        worksheet.merge_range(row_2, 0, row_2, 1, 'Advance Payment (EGP)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.Advance_Payment), add_format_emp_empty)
        row_2 = 12
        worksheet.merge_range(row_2, 0, row_2, 1, 'Retention', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.Retention), add_format_emp_empty)
        row_2 = 13
        worksheet.merge_range(row_2, 0, row_2, 1, 'Commencement Date', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, str(dashboard_obj.Commencement_Date), add_format_emp_empty)
        row_2 = 14
        worksheet.merge_range(row_2, 0, row_2, 1, 'Project Duration (Days)', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, (dashboard_obj.project_end_date - dashboard_obj.project_start_date).days,
                              add_format_emp_empty)
        row_2 = 15
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Consultant', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, dashboard_obj.main_consultant_res_partner_id.name, add_format_emp_empty)
        row_2 = 16
        worksheet.merge_range(row_2, 0, row_2, 1, 'The Contractor', add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, dashboard_obj.main_contractor_res_partner_id.name, add_format_emp_empty)
        row_2 = 17
        worksheet.merge_range(row_2, 0, row_2, 1, "The contractor's consultant", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, dashboard_obj.consultant_res_partner_id.name, add_format_emp_empty)
        row_2 = 18
        worksheet.merge_range(row_2, 0, row_2, 1, "The Sub Contractor", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, dashboard_obj.contractor_res_partner_id.name, add_format_emp_empty)
        row_2 = 19
        worksheet.merge_range(row_2, 0, row_2, 1, "The Sub contractor's consultant", add_format_emp1)
        worksheet.merge_range(row_2, 2, row_2, 4, dashboard_obj.consultant_res_partner_id.name, add_format_emp_empty)

        bold = workbook.add_format({"bold": 1})

        # Add the worksheet data that the charts will refer to.
        headings = ["Category", "Values"]
        data = [
            ['Elapsed Time', 'Remaining Time'],
            [round(dashboard_obj.elapsed_time * 100), round(dashboard_obj.remaining_time * 100)],
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
        remaining_time = (dashboard_obj.project_end_date - datetime.now().date()).days
        # chart1.set_title({"name": "Project Duration\nVariance (Days): " + str(remaining_time)})
        chart1.set_title({"name": "Project Duration(Days): " + str(remaining_time) + "\n Effective Variance(Days):" + str(int(dashboard_obj.date_variance))})
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
            [dashboard_obj.Project_Budget, dashboard_obj.Advance_Payment, dashboard_obj.Project_Budget - dashboard_obj.Advance_Payment],
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
        remaining_time = (dashboard_obj.project_end_date - datetime.now().date()).days
        chart2.set_title({"name": "Project Payment"})
        # Set an Excel chart style. Colors with white outline and shadow.
        chart2.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("F13", chart2, {"x_offset": 0, "y_offset": 0})
        #########Column Chart########################
        data = [["% Planned Comulative", "% Actual Comulative", "% Planned This Month", "% Actual This Month"],
                [dashboard_obj.current_ppp, dashboard_obj.current_pppp, dashboard_obj.current_wvcm, dashboard_obj.current_wvpm]]
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
        data = [["Work Completed Value Accourding to BOQ", "Work Planned Value Accourding to BOQ", "Total Budget"],
                [dashboard_obj.current_wcv, dashboard_obj.current_wpv, dashboard_obj.Project_Budget]]
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
        data = [
            ["Under Approval", "Approval", "Approved With Comments", "Revise And Resubmit", "Rejected", "Cancelled",
             "Revision", "Latest Documents", "Superseded Documents", "Opened Documents", "Closed Documents"],
            [dashboard_obj.h_co_action_code, dashboard_obj.a_co_action_code, dashboard_obj.b_co_action_code, dashboard_obj.c_co_action_code,
             dashboard_obj.d_co_action_code, dashboard_obj.cancel_co_action_code, dashboard_obj.revision_co_action_code, dashboard_obj.latest_dos,
             dashboard_obj.superseded_dos, dashboard_obj.opened_dosStatus, dashboard_obj.closed_dosStatus],
            [dashboard_obj.h_co_action_code1, dashboard_obj.a_co_action_code1, dashboard_obj.b_co_action_code1, dashboard_obj.c_co_action_code1,
             dashboard_obj.d_co_action_code1, dashboard_obj.cancel_co_action_code1, dashboard_obj.revision_co_action_code1, dashboard_obj.latest_dos1,
             dashboard_obj.superseded_dos1, dashboard_obj.opened_dosStatus1, dashboard_obj.closed_dosStatus1],
            [dashboard_obj.h_co_action_code2, dashboard_obj.a_co_action_code2, dashboard_obj.b_co_action_code2, dashboard_obj.c_co_action_code2,
             dashboard_obj.d_co_action_code2, dashboard_obj.cancel_co_action_code2, dashboard_obj.revision_co_action_code2, dashboard_obj.latest_dos2,
             dashboard_obj.superseded_dos2, dashboard_obj.opened_dosStatus2, dashboard_obj.closed_dosStatus2],
            [dashboard_obj.h_co_action_code3, dashboard_obj.a_co_action_code3, dashboard_obj.b_co_action_code3, dashboard_obj.c_co_action_code3,
             dashboard_obj.d_co_action_code3, dashboard_obj.cancel_co_action_code3, dashboard_obj.revision_co_action_code3, dashboard_obj.latest_dos3,
             dashboard_obj.superseded_dos3, dashboard_obj.opened_dosStatus3, dashboard_obj.closed_dosStatus3],
            [dashboard_obj.h_co_action_code4, dashboard_obj.a_co_action_code4, dashboard_obj.b_co_action_code4, dashboard_obj.c_co_action_code4,
             dashboard_obj.d_co_action_code4, dashboard_obj.cancel_co_action_code4, dashboard_obj.revision_co_action_code4, dashboard_obj.latest_dos4,
             dashboard_obj.superseded_dos4, dashboard_obj.opened_dosStatus4, dashboard_obj.closed_dosStatus4],
            [dashboard_obj.h_co_action_code5, dashboard_obj.a_co_action_code5, dashboard_obj.b_co_action_code5, dashboard_obj.c_co_action_code5,
             dashboard_obj.d_co_action_code5, dashboard_obj.cancel_co_action_code5, dashboard_obj.revision_co_action_code5, dashboard_obj.latest_dos5,
             dashboard_obj.superseded_dos5, dashboard_obj.opened_dosStatus5, dashboard_obj.closed_dosStatus5],
            [dashboard_obj.h_co_action_code6, dashboard_obj.a_co_action_code6, dashboard_obj.b_co_action_code6, dashboard_obj.c_co_action_code6,
             dashboard_obj.d_co_action_code6, dashboard_obj.cancel_co_action_code6, dashboard_obj.revision_co_action_code6, dashboard_obj.latest_dos6,
             dashboard_obj.superseded_dos6, dashboard_obj.opened_dosStatus6, dashboard_obj.closed_dosStatus6],
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
                "name": 'Document Submittal Logs',
                "categories": ["Sheet1", 21, 0, 33, 0],
                "values": ["Sheet1", 21, 1, 33, 1],
                'line': {'color': 'blue'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Document Submittal SD Logs",
                "categories": ["Sheet1", 21, 1, 33, 1],
                "values": ["Sheet1", 21, 2, 33, 2],
                'line': {'color': 'red'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Inspection Request Logs",
                "categories": ["Sheet1", 21, 2, 33, 2],
                "values": ["Sheet1", 21, 3, 33, 3],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Material Inspection Request Logs",
                "categories": ["Sheet1", 21, 3, 33, 3],
                "values": ["Sheet1", 21, 4, 33, 4],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Material Submittal Logs",
                "categories": ["Sheet1", 21, 4, 33, 4],
                "values": ["Sheet1", 21, 5, 33, 5],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Non Conformance Report Logs",
                "categories": ["Sheet1", 21, 5, 33, 5],
                "values": ["Sheet1", 21, 6, 33, 6],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        column_chart1.add_series(
            {
                "name": "Request For Information Logs",
                "categories": ["Sheet1", 21, 6, 33, 6],
                "values": ["Sheet1", 21, 7, 33, 7],
                'line': {'color': 'green'},
                'overlap': 10,
            }
        )
        column_chart1.set_title({"name": " Totals "})
        # column_chart1.set_x_axis({"name": "Submitted For"})
        column_chart1.set_y_axis({"name": "Totals", "major_units": 0.25, "num_format": "0"})

        # Set an Excel chart style.
        column_chart1.set_style(20)

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart("A22", column_chart1, {"x_offset": 0, "y_offset": 0, 'x_scale': 2.25, 'y_scale': 1.75})

        if self.env.user.lang == 'ar_SY':
            worksheet.right_to_left()
