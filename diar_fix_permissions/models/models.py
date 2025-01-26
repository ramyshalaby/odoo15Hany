# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    barcode = fields.Char(groups="base.group_user")
    permit_no = fields.Char(groups="base.group_user")
    pin = fields.Char(groups="base.group_user")
    spouse_complete_name = fields.Char(groups="base.group_user")
    study_field = fields.Char(groups="base.group_user")
    study_school = fields.Char(groups="base.group_user")
    total_overtime = fields.Float(groups="base.group_user")
    place_of_birth = fields.Char(groups="base.group_user")
    spouse_birthdate = fields.Date(groups="base.group_user")
    visa_expire = fields.Date(groups="base.group_user")
    address_home_id = fields.Many2one(groups="base.group_user")
    hours_last_month_display = fields.Char(groups="base.group_user")
    emergency_contact = fields.Char(groups="base.group_user")
    visa_no = fields.Char(groups="base.group_user")
    emergency_phone = fields.Char(groups="base.group_user")
    employee_phone = fields.Char(groups="base.group_user")
    passport_id = fields.Char(groups="base.group_user")
    certificate = fields.Selection(groups="base.group_user")
    attendance_state = fields.Selection(groups="base.group_user")
    children = fields.Integer(groups="base.group_user")
    km_home_work = fields.Integer(groups="base.group_user")
    country_of_birth = fields.Many2one(groups="base.group_user")
    employee_bank_account_id = fields.Many2one(groups="base.group_user")
    employee_country_id = fields.Many2one(groups="base.group_user")
    identification_id = fields.Char(groups="base.group_user")
    gender = fields.Selection(groups="base.group_user")
    marital = fields.Selection(groups="base.group_user")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    address_home_id = fields.Many2one(groups="base.group_user")
    bank_account_id = fields.Many2one(groups="base.group_user")
    country_id = fields.Many2one(groups="base.group_user")
    km_home_work = fields.Integer(groups="base.group_user")

