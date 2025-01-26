from odoo import models, fields, api, _
from datetime import datetime

from odoo.exceptions import ValidationError


class TimesheetValidation(models.Model):
	_inherit = 'account.analytic.line'

	approved = fields.Boolean('Approved')
	approved_user_id = fields.Many2one('res.users', string='Approved By')
	approved_date = fields.Datetime('Approved Date')

	refused = fields.Boolean('Refuse')
	refused_user_id = fields.Many2one('res.users', string='Refused By')
	refused_date = fields.Datetime('Refused Date')
	unit_amount_cost = fields.Monetary(compute="calc_unit_amount_cost", string="Unit Amount Cost", store=True)
	worked_hours = fields.Float('Work Hours', compute="calc_worked_hours")


	@api.depends('date', 'employee_id')
	@api.onchange('date', 'employee_id')
	def calc_worked_hours(self):
		for record in self:
			hr_attendance_objs = self.env['hr.attendance'].sudo().search(
				[('employee_id', '=', record.employee_id.id), ('check_in', '<=', record.date),
				 ('check_out', '>=', record.date)])
			record.worked_hours = sum(hr_attendance_obj.worked_hours for hr_attendance_obj in hr_attendance_objs)

	@api.constrains('employee_id', 'date', 'unit_amount')
	def check_timesheet_per_attendance(self):
		for record in self:
			if record.employee_id and record.date and record.unit_amount:
				account_analytic_line_objs = self.env['account.analytic.line'].sudo().search([(('employee_id','=',record.employee_id.id)), ('date','=',record.date)])
				total_timesheet_unit_amount  = sum(account_analytic_line_obj.unit_amount for account_analytic_line_obj in account_analytic_line_objs)
				hr_leave_objs = self.env['hr.leave'].sudo().search([(('employee_id','=',record.employee_id.id)), ('date_from','<=',record.date), ('date_to','>=',record.date),('state','=','validate')])
				hr_attendance_objs = self.env['hr.attendance'].sudo().search([('employee_id','=',record.employee_id.id), ('check_in','<=',record.date),('check_out','>=',record.date)])
				if not hr_attendance_objs and not hr_leave_objs:
					raise ValidationError(_("Sorry you can't create timesheet in this day as theres no attendance record or leave record or mission record"))
				for hr_attendance_obj in hr_attendance_objs:
					if total_timesheet_unit_amount > hr_attendance_obj.worked_hours:
						raise ValidationError(
							_("Sorry you can't create timesheet in this day as Hours spent is greater than worked hours in attendance"))

	@api.onchange('employee_id.timesheet_cost', 'unit_amount')
	@api.depends('employee_id.timesheet_cost', 'unit_amount')
	def calc_unit_amount_cost(self):
		for record in self:
			record.unit_amount_cost = record.employee_id.sudo().timesheet_cost*record.unit_amount

	def approve(self):
		for record in self:
			record.approved = True
			record.approved_user_id = self.env.user.id
			record.approved_date = datetime.now()
			mail_template = self.env.ref('diar_timesheet_approval.timesheet_validation_email_template')
			mail_template.send_mail(record.id, force_send=True)

	def refuse(self):
		for record in self:
			record.refused = True
			record.refused_user_id = self.env.user.id
			record.refused_date = datetime.now()
			mail_template = self.env.ref('diar_timesheet_approval.timesheet_refused_validation_email_template')
			mail_template.send_mail(record.id, force_send=True)
