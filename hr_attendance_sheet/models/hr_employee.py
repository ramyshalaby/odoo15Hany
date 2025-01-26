from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def calculate_parttime_action(self, date_from, date_to):
        attendance_sheet_line_objs = self.env['attendance.sheet.line'].search(
            [('att_sheet_id.state', '=', 'done'), ('date', '>=', date_from), ('date', '<=', date_to),
             ('att_sheet_id.employee_id', '=', self.id)])
        amount_per_hour = 0.0
        for attendance_sheet_line_obj in attendance_sheet_line_objs:
            amount_per_hour += self.timesheet_cost * attendance_sheet_line_obj.worked_hours
        return amount_per_hour
