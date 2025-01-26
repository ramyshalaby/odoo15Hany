from odoo import models, fields, api
from datetime import datetime

class OvertimeCalcualator(models.Model):
    _name = 'overtime.calculator'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_employee(self):
        return self.env.user.employee_id

    name = fields.Char( string="Ref")
    start_date = fields.Date(string="Start Date",tracking=True,)
    end_date = fields.Date(string="End Date",tracking=True,)
    employee_id = fields.Many2one('hr.employee',string="Employee",tracking=True,default = _default_employee)
    department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id")
    # manager_id = fields.Many2one('hr.employee', string="Manager",related="employee_id.partner_id")
    approved_date = fields.Date(string="Approved Date",tracking=True,)
    requested_by = fields.Many2one('hr.employee',string="Requested By",tracking=True,)
    requesting_reason = fields.Text(string="Request Reason")
    rejection_reason = fields.Text(string="Rejection Reason")
    hours = fields.Float(string="Total worked hours",tracking=True,)
    contract_id = fields.Many2one('hr.contract', string="Contract", related='employee_id.contract_id')
    currency_id = fields.Many2one('res.currency', related='contract_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('department_approve', 'Department Approved'),
        ('reject', 'Rejected'),
        ('hr_approve', 'HR Approved'),
        ('gm_approve', 'GM Approved'),
        ('paid', 'Paid')
        ], string="state", default="draft",tracking=True,)
    overtime_type_id = fields.Many2one('overtime.rate', string="Overtime type",tracking=True,)

    value = fields.Float(string='Value', compute="_compute_value", store=True, tracking=True,)
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('overtime.calculator') or _('New')
        return super(OvertimeCalcualator, self).create(vals)

    @api.depends('employee_id', 'hours', 'overtime_type_id')
    def _compute_value(self):
            # for rec in self:
              for contract in self.env['hr.contract'].search(['&',('employee_id','=', self.employee_id.id),('state','=','open')]):
                    # if contract:
                        type = self.env['overtime.rate'].search([('id','=',self.overtime_type_id.id)])

                        weekly_hours = self.env['resource.calendar'].search([('id', '=', contract.resource_calendar_id.id)])

                        total_hours = weekly_hours.weekly_working_hour * 4
                        # total_hours = 4
                        if total_hours > 0:
                            salary_per_hour = contract.wage / total_hours

                            if type.name == "normal":
                                self.value = salary_per_hour * type.rate * self.hours
                            elif type.name == "night":
                                self.value = salary_per_hour * type.rate * self.hours
                            elif type.name == "sunday":
                                self.value = salary_per_hour * type.rate * self.hours
                            elif type.name== "holiday":
                                self.value = salary_per_hour * type.rate * self.hours
                            else:
                                self.value = 0.0
                        else:
                         self.value = 0.0


    # overtime_line_ids = fields.One2many('overtime.lines', 'overtime_id', string='Overtime')

    def action_submit(self):
        self.state = 'submit'

    def action_dept_approve(self):
        self.state = 'department_approve'

    def action_reject(self):
        self.state = 'reject'

    def action_gm_apprve(self):
        self.state = 'gm_approve'

    def action_paid(self):
            self.state = 'paid'
    def action_hr(self):
            self.state = 'hr_approve'



class OvertimeRate(models.Model):
    _name = 'overtime.rate'

    name = fields.Selection([
                                      ('normal','Regular day'),
                                      ('night','Regular night'),
                                      ('sunday', 'Sunday'),
                                      ('holiday', 'Holiday')
                                      ], string="Overtime type")
    rate = fields.Float(string="Rate")


class WorkingWeek(models.Model):
    _inherit = 'resource.calendar'


    weekly_working_hour = fields.Float(string='Weekly Working Hour')
    # total_hour = fields.Float(string='Total Hour', comute="_get_total")



