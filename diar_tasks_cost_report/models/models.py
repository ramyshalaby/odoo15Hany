# -*- coding: utf-8 -*-
import json
import io
from xlsxwriter import workbook

from odoo.tools import date_utils
from odoo import fields, models, api

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    month_hours = fields.Float(compute="_compute_hours", store=True)
    weekdays = fields.Float(compute="_compute_hours", store=True)

    @api.depends('attendance_ids', 'hours_per_day')
    def _compute_hours(self):
        for rec in self:
            days = []
            for att in rec.attendance_ids:
                if att.dayofweek not in days:
                    days.append(att.dayofweek)
            rec.weekdays = len(days)
            rec.month_hours = len(days) * 4 * rec.hours_per_day



class DiarTasksAdvance(models.TransientModel):
    _name = "diar.tasks.report"

    employee_ids = fields.Many2many('hr.employee', required=False)
    from_date = fields.Date(string="Start Date", required=True)
    to_date = fields.Date(string="End Date", required=True)

    def get_diar_tasks_report(self):
        datas = self._get_data()
        return self.env.ref('diar_tasks_cost_report.action_diar_tasks_analysis').report_action([], data=datas)

    def _get_data(self):
        timesheet = self.env['account.analytic.line'].search([('employee_id', 'in', self.employee_ids.ids)])
        result = []
        resultemp = []
        employees = self.employee_ids
        if not employees:
            employees = self.env['hr.employee'].search([])
        for single_date in daterange(self.from_date, self.to_date):
            empdatetimesheet = list(filter(lambda x: x.date == single_date, timesheet))
            for employee in employees:
                emptimesheet = list(filter(lambda x: x.employee_id.id >= employee.id, empdatetimesheet))


                projects = [list(res.values())[1] for res in
                            self.env['account.analytic.line'].search_read([
                                ('employee_id', '=', employee.ids),
                                ('date', '=', single_date)
                            ], ['project_id'])]
                resultpro = []
                print('projects === ', projects)
                total_amount = 0
                project_cost = 0
                for p in projects:
                    amount = 0
                    for t in emptimesheet:
                        if t.project_id.id == p[0]:
                            amount += t.unit_amount
                    if amount:
                        resultpro.append({
                            'emp': t.employee_id.name,
                            'project': p[1],
                            'date': single_date,
                            'amount': amount,
                            'project_cost': employee.timesheet_cost * amount
                        })
                        project_cost += employee.timesheet_cost * amount
                        total_amount += amount
                if resultpro:
                    hour_cost_contract = employee.contract_id.wage/196 if employee.contract_id else 0
                    day_cost_contract = employee.contract_id.resource_calendar_id.hours_per_day * hour_cost_contract if employee.contract_id else 0
                    resultemp.append({
                        'date': single_date.strftime("%Y-%m-%d"),
                        'emp': employee.name,
                        employee.name: resultpro,
                        'hour_cost_sheet': employee.timesheet_cost,
                        'hour_cost_contract': hour_cost_contract,
                        'day_cost_actual': day_cost_contract, #hour_cost_contract
                        'over_head': day_cost_contract - project_cost #hour_cost_contract
                    })
                resultpro = []
            if resultemp:
                result.append({'date': single_date.strftime("%Y-%m-%d"),
                               single_date.strftime("%Y-%m-%d"): resultemp})
            resultemp = []

        # sale = self.env['sale.order'].search([('state', '!=', 'cancel')])
        # sales_order = sale
        # if self.from_date and not self.to_date:
        #     pass
        #     # sales_order = list(filter(lambda x: x.date_order.date() >= self.from_date, sale))
        #
        # result = []
        #
        # for so in sales_order:
        #     res = {
        #         'so': so.name,
        #         'partner_id': so.partner_id,
        #         'order_date': so.date_order,
        #         'invoice': so.name,
        #         # 'ref': so.ref,
        #         # 'unit': so.operating_unit_id.name,
        #         # 'date': so.invoice_date,
        #         # 'invoiced': so.amount_total,
        #         # 'paid': so.amount_total - so.amount_residual,
        #         # 'due': so.amount_residual,
        #     }
        #     result.append(res)
        datas = {
            'ids': self,
            'model': 'diar.tasks.report',
            'form': result,
            'start_date': self.from_date,
            'end_date': self.to_date,
        }

        return datas

    def get_excel_diar_tasks_report(self):
        datas = self._get_data()

        return self.env.ref('diar_tasks_cost_report.action_diar_tasks_report_xlsx').report_action(self,
            data=datas)

class WarehouseReportXlsx(models.AbstractModel):
    _name = 'report.diar_tasks_cost_report.report_tasks_cost_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', })
        head = workbook.add_format()
        head.set_font_size(20)
        head.set_bold()
        head.set_align('center')
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('G2:M3', 'Project Cost per employee', head)
        if data['start_date'] and data['end_date']:
            sheet.write('G5', 'From:', cell_format)
            sheet.merge_range('H5:I5', data['start_date'], txt)
            sheet.write('K5', 'To:', cell_format)
            sheet.merge_range('L5:M5', data['end_date'], txt)

        format1 = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'bg_color': '#bbd5fc', 'border': 1})
        format4 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#bbd5fc', 'border': 1})
        format2 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bold': True,
             'bg_color': '#6BA6FE', 'border': 1})
        format3 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bold': True})
        row_number = 7
        print("data = ", data)

        for val in data['form']:
            row_number += 1
            column_number = 2
            c = row_number
            for datee in val[val['date']]:
                d = row_number
                for line in datee[datee['emp']]:
                    sheet.write(row_number, 9, line['project'], format1)
                    sheet.write(row_number, 7, line['amount'], format1)
                    sheet.write(row_number, 10, line['project_cost'], format1)
                if d != row_number:
                    sheet.merge_range(f'B{d}:B{row_number}', val['date'], format1)
                    sheet.merge_range(f'C{d}:C{row_number}', val['date'][5:7], format1)
                    sheet.merge_range(f'D{d}:D{row_number}', val['date'][:4], format1)
                    sheet.merge_range(f'E{d}:E{row_number}', datee['emp'], format1)
                    sheet.merge_range(f'F{d}:F{row_number}', datee['hour_cost_sheet'], format1)
                    sheet.merge_range(f'G{d}:G{row_number}', datee['hour_cost_contract'], format1)
                    sheet.merge_range(f'I{d}:I{row_number}', '8', format1)
                    sheet.merge_range(f'L{d}:L{row_number}',  datee['day_cost_actual'], format1)
                    sheet.merge_range(f'M{d}:M{row_number}',  datee['over_head'], format1)
                else:
                    sheet.write(row_number, 1, val['date'], format1)
                    sheet.write(row_number, 2, val['date'][5:7], format1)
                    sheet.write(row_number, 3, val['date'][:4], format1)
                    sheet.write(row_number, 4, datee['emp'], format1)
                    sheet.write(row_number, 5, datee['hour_cost_sheet'], format1)
                    sheet.write(row_number, 6, datee['hour_cost_contract'], format1)
                    sheet.write(row_number, 8, '8', format1)
                    sheet.write(row_number, 11,  datee['day_cost_actual'], format1)
                    sheet.write(row_number, 12,  datee['over_head'], format1)

                row_number += 1
            # formula = '=SUM(Table8[@[Quarter 1]:[Quarter 4]])'
            sheet.add_table(f'B{c}:M{row_number}',
                            {'columns': [{'header': 'Date'},
                                         {'header': 'Month'},
                                         {'header': 'Year'},
                                         {'header': 'Employee'},
                                         {'header': 'Hour rate from Time sheet'},
                                         {'header': 'Hour rate from Contract'},
                                         {'header': 'Number of hour from time sheet '},
                                         {'header': 'Number of hour from finger print'},
                                         {'header': 'Project per Employee'},
                                         {'header': 'Estimated Salary per Project'},
                                         {'header': 'Gross Actual Salary'},
                                         {'header': 'Over Head Cost'},
                                         # {'formula': formula},
                                          ]})
            # 'Date'
            # 'Month'
            # 'Year'
            # 'Employee'
            # 'Hour rate from Time sheet'
            # 'Hour rate from Contract'
            # 'Number of hour from time sheet '
            # 'Number of hour from finger print'
            # 'Estimated Salary per Project'
            # 'Gross Actual Salary'
            # 'Over Head Cost'
            row_number += 1
        if not data['form']:
            sheet.add_table(f'B{row_number}:M{row_number+1}',
                {'columns': [{'header': 'Date'},
                             {'header': 'Month'},
                             {'header': 'Year'},
                             {'header': 'Employee'},
                             {'header': 'Hour rate from Time sheet'},
                             {'header': 'Hour rate from Contract'},
                             {'header': 'Number of hour from time sheet '},
                             {'header': 'Number of hour from finger print'},
                             {'header': 'Project per Employee'},
                             {'header': 'Estimated Salary per Project'},
                             {'header': 'Gross Actual Salary'},
                             {'header': 'Over Head Cost'},
                             # {'formula': formula},
                             ]})
        # workbook.close()
        # output.seek(0)
        # response.stream.write(output.read())
        # output.close()
