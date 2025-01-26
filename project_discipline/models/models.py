# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectDeliverablesType(models.Model):
    _name = 'project.deliverables.type'
    _rec_name = 'name'
    _description = 'Project Deliverables Type'

    name = fields.Char(string="Document Type", required=True, )


class ProjectEngineeringPhase(models.Model):
    _name = 'project.engineering.phase'
    _rec_name = 'name'
    _description = 'Project Engineering Phase'

    name = fields.Char(string="Engineering Phase", required=True, )


class ProjectDeliverables(models.Model):
    _name = 'project.deliverables'
    _rec_name = 'name'
    _description = 'Project Deliverables'

    name = fields.Char(string="Document Title", required=True, )
    discipline_id = fields.Many2one(comodel_name="hr.department", string="Discipline", required=True, )
    engineering_phase_id = fields.Many2one(comodel_name='project.engineering.phase', string="Engineering Phase", required=True, )
    deliverable_type_id = fields.Many2one(comodel_name="project.deliverables.type", string="Document Type", required=True, )
    remarks = fields.Text(string="Remarks", required=False, )


class ResourceValue(models.Model):
    _name = 'resource.value'
    _rec_name = 'job_id'
    _description = 'Resource Value'

    job_id = fields.Many2one(comodel_name="hr.job", string="Resource Title", required=True, )
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda x: x.env.company.currency_id)
    resource_value = fields.Monetary(string="Cost", currency_field="currency_id",required=True, )
    uom_id = fields.Many2one(comodel_name="uom.uom", string="UoM", domain=lambda s: [('category_id', '=', s.env.ref('uom.uom_categ_wtime').id)])
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True, )


class Department(models.Model):
    _name = 'hr.department'
    _inherit = 'hr.department'

    resource_value_ids = fields.One2many(comodel_name="resource.value", inverse_name="department_id", string="Resources Values", required=False, )


class ProjectType(models.Model):
    _name = 'project.type'
    _rec_name = 'name'
    _description = 'Project Type'

    name = fields.Char(string="Type", required=True, )


class ProjectEstimation(models.Model):
    _name = 'project.estimation'
    _order = 'id DESC'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Estimation'

    name = fields.Char(string="Description", required=True, tracking=True)
    project_name = fields.Char(string="Project Name", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', readonly=True, default=lambda x: x.env.company.currency_id)
    total_request = fields.Monetary(string="Request Total", currency_field="currency_id", compute="_compute_total_amounts", )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, tracking=True)
    department_ids = fields.Many2many(comodel_name="hr.department", relation="project_estimation_department_rel", column1="estimation_id", column2="department_id", string="Assigned to", )
    project_type_id = fields.Many2one(comodel_name="project.type", string="Project Type", required=False, )
    created_on = fields.Datetime(string="Created On", required=False, default=fields.Datetime.now)
    deadline = fields.Date(string="Deadline", required=True, tracking=True)
    creator_id = fields.Many2one(comodel_name="res.users", string="Created By", default=lambda s: s.env.user.id, )
    notes = fields.Html(string="Notes", )
    # Configurations
    is_fire_fighting_pluming = fields.Boolean(string="Fire Fighting & Pluming", )
    fire_fighting_pluming_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'fire fighting')], limit=1).id)
    fire_fighting_pluming_department_manager_user_id = fields.Many2one(related="fire_fighting_pluming_department_id.manager_id.user_id")
    is_fire_fighting_pluming_department_manager_user_id = fields.Boolean(string="is fire_fighting_pluming_department_manager_user_id", compute="_compute_owner")

    is_hvac = fields.Boolean(string="HVAC", )
    hvac_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'HVAC')], limit=1).id)
    hvac_department_manager_user_id = fields.Many2one(related="hvac_department_id.manager_id.user_id")
    is_hvac_department_manager_user_id = fields.Boolean(string="is hvac_department_manager_user_id", compute="_compute_owner" )

    is_instrumentation = fields.Boolean(string="Instrumentation", )
    instrumentation_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'instrumentation')], limit=1).id)
    instrumentation_department_manager_user_id = fields.Many2one(related="instrumentation_department_id.manager_id.user_id")
    is_instrumentation_department_manager_user_id = fields.Boolean(string="is instrumentation_department_manager_user_id", compute="_compute_owner" )

    is_architect = fields.Boolean(string="Architect", )
    architect_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'architect')], limit=1).id)
    architect_department_manager_user_id = fields.Many2one(related="architect_department_id.manager_id.user_id")
    is_architect_department_manager_user_id = fields.Boolean(string="is architect_department_manager_user_id", compute="_compute_owner" )

    is_civil = fields.Boolean(string="Civil", )
    civil_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'civil')], limit=1).id)
    civil_department_manager_user_id = fields.Many2one(related="civil_department_id.manager_id.user_id")
    is_civil_department_manager_user_id = fields.Boolean(string="is civil_department_manager_user_id", compute="_compute_owner" )

    is_document_controller = fields.Boolean(string="Document Controller", )
    document_controller_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'Document Controller')], limit=1).id)
    document_controller_department_manager_user_id = fields.Many2one(related="document_controller_department_id.manager_id.user_id")
    is_document_controller_department_manager_user_id = fields.Boolean(string="is document_controller_department_manager_user_id", compute="_compute_owner" )

    is_electrical = fields.Boolean(string="Electrical", )
    electrical_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'electrical')], limit=1).id)
    electrical_department_manager_user_id = fields.Many2one(related="electrical_department_id.manager_id.user_id")
    is_electrical_department_manager_user_id = fields.Boolean(string="is electrical_department_manager_user_id", compute="_compute_owner" )

    is_hse = fields.Boolean(string="HSE", )
    hse_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'hse')], limit=1).id)
    hse_department_manager_user_id = fields.Many2one(related="hse_department_id.manager_id.user_id")
    is_hse_department_manager_user_id = fields.Boolean(string="is hse_department_manager_user_id", compute="_compute_owner" )

    is_low_current = fields.Boolean(string="Low Current", )
    low_current_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'Low Current')], limit=1).id)
    low_current_department_manager_user_id = fields.Many2one(related="low_current_department_id.manager_id.user_id")
    is_low_current_department_manager_user_id = fields.Boolean(string="is low_current_department_manager_user_id", compute="_compute_owner" )

    is_management = fields.Boolean(string="Management", )
    management_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'management')], limit=1).id)
    management_department_manager_user_id = fields.Many2one(related="management_department_id.manager_id.user_id")
    is_management_department_manager_user_id = fields.Boolean(string="is management_department_manager_user_id", compute="_compute_owner" )

    is_piping = fields.Boolean(string="Piping", )
    piping_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'piping')], limit=1).id)
    piping_department_manager_user_id = fields.Many2one(related="piping_department_id.manager_id.user_id")
    is_piping_department_manager_user_id = fields.Boolean(string="is piping_department_manager_user_id", compute="_compute_owner" )

    is_process = fields.Boolean(string="Process", )
    process_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'process')], limit=1).id)
    process_department_manager_user_id = fields.Many2one(related="process_department_id.manager_id.user_id")
    is_process_department_manager_user_id = fields.Boolean(string="is process_department_manager_user_id", compute="_compute_owner" )

    is_top_management = fields.Boolean(string="Top Management", )
    top_management_department_id = fields.Many2one(comodel_name="hr.department", string="Department", default=lambda s: s.env['hr.department'].search([('name', 'ilike', 'Top Management')], limit=1).id)
    top_management_department_manager_user_id = fields.Many2one(related="top_management_department_id.manager_id.user_id")
    is_top_management_department_manager_user_id = fields.Boolean(string="is top_management_department_manager_user_id", compute="_compute_owner" )
    # Pages Lines
    fire_fighting_pluming_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="fire_fighting_pluming_id", string="Fire Fighting & Pluming Estimation", required=False, )
    total_fire_fighting_pluming = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    instrumentation_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="instrumentation_lines_id", string="Instrumentation Estimation", required=False, )
    total_instrumentation_lines = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    hvac_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="hvac_id", string="HVAC Estimation", required=False, )
    total_hvac = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    architect_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="architect_id", string="Architect Estimation", required=False, )
    total_architect = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    civil_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="civil_id", string="Civil Estimation", required=False, )
    total_civil = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    document_controller_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="document_controller_id", string="Document Controller Estimation", required=False, )
    total_document_controller = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    electrical_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="electrical_id", string="Electrical Estimation", required=False, )
    total_electrical = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    hse_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="hse_id", string="HSE Estimation", required=False, )
    total_hse = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")
    
    low_current_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="low_current_id", string="Low Current Estimation", required=False, )
    total_low_current = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    management_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="management_id", string="Management Estimation", required=False, )
    total_management = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    piping_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="piping_id", string="Piping Estimation", required=False, )
    total_piping = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    process_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="process_id", string="Process Estimation", required=False, )
    total_process = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    top_management_lines_ids = fields.One2many(comodel_name="project.estimation.line", inverse_name="top_management_id", string="Top Management Estimation", required=False, )
    total_top_management = fields.Monetary(string="Total", currency_field="currency_id", compute="_compute_total_amounts")

    is_request_creator = fields.Boolean(string="Is Request Creator?", compute="_compute_is_request_creator")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancel')], default="draft", )
    project_id = fields.Many2one(comodel_name="project.project", string="Project", required=False, )

    @api.depends('top_management_lines_ids', 'process_lines_ids', 'piping_lines_ids', 'management_lines_ids', 'low_current_lines_ids', 'hse_lines_ids', 'architect_lines_ids', 'electrical_lines_ids', 'document_controller_lines_ids', 'civil_lines_ids', 'fire_fighting_pluming_lines_ids', 'instrumentation_lines_ids', 'hvac_lines_ids')
    def _compute_total_amounts(self):
        for rec in self:
            rec.total_fire_fighting_pluming = sum([line.subtotal for line in rec.fire_fighting_pluming_lines_ids])
            rec.total_instrumentation_lines = sum([line.subtotal for line in rec.instrumentation_lines_ids])
            rec.total_hvac = sum([line.subtotal for line in rec.hvac_lines_ids])
            rec.total_architect = sum([line.subtotal for line in rec.architect_lines_ids])
            rec.total_civil = sum([line.subtotal for line in rec.civil_lines_ids])
            rec.total_document_controller = sum([line.subtotal for line in rec.document_controller_lines_ids])
            rec.total_electrical = sum([line.subtotal for line in rec.electrical_lines_ids])
            rec.total_hse = sum([line.subtotal for line in rec.hse_lines_ids])
            rec.total_low_current = sum([line.subtotal for line in rec.low_current_lines_ids])
            rec.total_management = sum([line.subtotal for line in rec.management_lines_ids])
            rec.total_piping = sum([line.subtotal for line in rec.piping_lines_ids])
            rec.total_process = sum([line.subtotal for line in rec.process_lines_ids])
            rec.total_top_management = sum([line.subtotal for line in rec.top_management_lines_ids])
            
            rec.total_request = sum([rec.total_top_management, rec.total_process, rec.total_piping, rec.total_management,
                                     rec.total_low_current, rec.total_hse, rec.total_electrical, rec.total_civil,
                                     rec.total_document_controller, rec.total_fire_fighting_pluming, rec.total_hvac,
                                     rec.total_instrumentation_lines, rec.total_architect, ])
    def get_partners(self):
        users_list = []
        if self.is_fire_fighting_pluming:
            users_list.append(self.fire_fighting_pluming_department_manager_user_id)
        if self.is_hvac:
            users_list.append(self.hvac_department_manager_user_id)
        if self.is_instrumentation:
            users_list.append(self.instrumentation_department_manager_user_id)
        if self.is_architect:
            users_list.append(self.architect_department_manager_user_id)
        if self.is_civil:
            users_list.append(self.civil_department_manager_user_id)
        if self.is_document_controller:
            users_list.append(self.document_controller_department_manager_user_id)
        if self.is_electrical:
            users_list.append(self.electrical_department_manager_user_id)
        if self.is_hse:
            users_list.append(self.hse_department_manager_user_id)
        if self.is_low_current:
            users_list.append(self.low_current_department_manager_user_id)
        if self.is_management:
            users_list.append(self.management_department_manager_user_id)
        if self.is_piping:
            users_list.append(self.piping_department_manager_user_id)
        if self.is_process:
            users_list.append(self.process_department_manager_user_id)
        if self.is_top_management:
            users_list.append(self.top_management_department_manager_user_id)

        if users_list:
            return [user.partner_id for user in users_list]
        return []

    def set_mail_activity(self):
        env_mail_activity = self.env['mail.activity']
        activity_type_id = self.env.ref('project_discipline.project_discipline_mail_activity_type').id
        partner_ids = self.get_partners()
        if partner_ids:
            self.message_subscribe(partner_ids=[p.id for p in partner_ids])
            for partner in partner_ids:
                if partner.user_ids:
                    user = partner.user_ids[0]
                    env_mail_activity.with_context({
                        'active_model': self._name,
                        'active_id': self.id,
                        'default_res_id': self.id,
                        'default_res_model_id': self.env.ref('project_discipline.model_project_estimation').id
                    }).create({'user_id': user.id, 'activity_type_id': activity_type_id, 'summary': self.name})

    def set_progress(self):
        # Attachments are required, there should be one attached file at least.
        if self.message_attachment_count:
            self.state = 'progress'
            self.set_mail_activity()
        else:
            raise UserError(_("There should be one attachment at least!\nPlease, attach the files for this estimation."))

    def create_tasks(self, main_task, manager, lines):
        env_task = self.env['project.task'].with_context({'default_project_id': self.project_id.id})
        main_task_obj = env_task.create({'name': main_task, 'user_ids': [(4, manager.id)]})
        users = [(4, manager.id)]
        for line in lines:
            if line.employee_id.user_id.id:
                users.append((4, line.employee_id.user_id.id))
            env_task.create({'parent_id': main_task_obj.id, 'name': line.project_deliverables_id.name,
                             'project_deliverables_id': line.project_deliverables_id.id, 'user_ids': users})

    def create_project(self):
        env_project = self.env['project.project']
        project_obj = env_project.create({'name': self.project_name, 'partner_id': self.partner_id.id})
        self.project_id = project_obj.id
        if self.is_fire_fighting_pluming:
            main_task = "Fire Fighting & Pluming"
            self.create_tasks(main_task, self.fire_fighting_pluming_department_manager_user_id, self.fire_fighting_pluming_lines_ids)
        if self.is_hvac:
            main_task = "HVAC"
            self.create_tasks(main_task, self.hvac_department_manager_user_id, self.hvac_lines_ids)
        if self.is_instrumentation:
            main_task = "Instrumentation"
            self.create_tasks(main_task, self.instrumentation_department_manager_user_id, self.instrumentation_lines_ids)
        if self.is_architect:
            main_task = "Architect"
            self.create_tasks(main_task, self.architect_department_manager_user_id, self.architect_lines_ids)
        if self.is_civil:
            main_task = "Civil"
            self.create_tasks(main_task, self.civil_department_manager_user_id, self.civil_lines_ids)
        if self.is_document_controller:
            main_task = "Document Controller"
            self.create_tasks(main_task, self.document_controller_department_manager_user_id, self.document_controller_lines_ids)
        if self.is_electrical:
            main_task = "Electrical"
            self.create_tasks(main_task, self.electrical_department_manager_user_id, self.electrical_lines_ids)
        if self.is_hse:
            main_task = "HSE"
            self.create_tasks(main_task, self.hse_department_manager_user_id, self.hse_lines_ids)
        if self.is_low_current:
            main_task = "Low Current"
            self.create_tasks(main_task, self.low_current_department_manager_user_id, self.low_current_lines_ids)
        if self.is_management:
            main_task = "Management"
            self.create_tasks(main_task, self.management_department_manager_user_id, self.management_lines_ids)
        if self.is_piping:
            main_task = "Piping"
            self.create_tasks(main_task, self.piping_department_manager_user_id, self.piping_lines_ids)
        if self.is_process:
            main_task = "Process"
            self.create_tasks(main_task, self.process_department_manager_user_id, self.process_lines_ids)
        if self.is_top_management:
            main_task = "Top Management"
            self.create_tasks(main_task, self.top_management_department_manager_user_id, self.top_management_lines_ids)
        if project_obj:
            return True

    def set_done(self):
        allow_sub_task = self.env.user.has_group('project.group_subtask_project')
        if not allow_sub_task:
            raise UserError(_('Sub Tasks are not enabled for the current user!\nPlease, Contact Administrator.'))
        created_project = self.create_project()
        if created_project:
            self.state = 'done'
        else:
            raise UserError(_("Something went wrong while creating a project!"))

    def set_cancel(self):
        self.state = 'cancel'

    def set_draft(self):
        self.state = 'draft'

    @api.depends()
    def _compute_owner(self):
        current_user = self.env.user
        for rec in self:
            rec.is_fire_fighting_pluming_department_manager_user_id = rec.fire_fighting_pluming_department_manager_user_id == current_user
            rec.is_instrumentation_department_manager_user_id = rec.instrumentation_department_manager_user_id == current_user
            rec.is_hvac_department_manager_user_id = rec.hvac_department_manager_user_id == current_user
            rec.is_architect_department_manager_user_id = rec.architect_department_manager_user_id == current_user
            rec.is_civil_department_manager_user_id = rec.civil_department_manager_user_id == current_user
            rec.is_document_controller_department_manager_user_id = rec.document_controller_department_manager_user_id == current_user
            rec.is_electrical_department_manager_user_id = rec.electrical_department_manager_user_id == current_user
            rec.is_hse_department_manager_user_id = rec.hse_department_manager_user_id == current_user
            rec.is_low_current_department_manager_user_id = rec.low_current_department_manager_user_id == current_user
            rec.is_management_department_manager_user_id = rec.management_department_manager_user_id == current_user
            rec.is_piping_department_manager_user_id = rec.piping_department_manager_user_id == current_user
            rec.is_process_department_manager_user_id = rec.process_department_manager_user_id == current_user
            rec.is_top_management_department_manager_user_id = rec.top_management_department_manager_user_id == current_user

    @api.depends()
    def _compute_is_request_creator(self):
        for rec in self:
            rec.is_request_creator = self.env.user.has_group('sales_team.group_sale_manager')


class ProjectEstimationLines(models.Model):
    _name = 'project.estimation.line'
    _rec_name = 'resource_id'
    _description = 'Project Estimation Line'

    resource_id = fields.Many2one(comodel_name="resource.value", string="Job Position", required=True, )
    project_deliverables_id = fields.Many2one(comodel_name="project.deliverables", string="Task", required=False, )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Resource", required=False, )
    uom_id = fields.Many2one(related="resource_id.uom_id")
    qty = fields.Float(string="Qty",  required=False, default=0.0)
    currency_id = fields.Many2one(related="resource_id.currency_id")
    hourly_rate = fields.Monetary(string="Hourly Rate", related="resource_id.resource_value", store=True)
    subtotal = fields.Monetary(string="Subtotal", currency_field="currency_id", compute="_compute_subtotal", )
    fire_fighting_pluming_id = fields.Many2one(comodel_name="project.estimation", string="Fire Fighting & Pluming Estimation", required=False, )
    instrumentation_lines_id = fields.Many2one(comodel_name="project.estimation", string="Instrumentation Estimation", required=False, )
    hvac_id = fields.Many2one(comodel_name="project.estimation", string="HVAC Estimation", required=False, )
    architect_id = fields.Many2one(comodel_name="project.estimation", string="Architect Estimation", required=False, )
    civil_id = fields.Many2one(comodel_name="project.estimation", string="Civil Estimation", required=False, )
    document_controller_id = fields.Many2one(comodel_name="project.estimation", string="Document Controller Estimation", required=False, )
    electrical_id = fields.Many2one(comodel_name="project.estimation", string="Electrical Estimation", required=False, )
    hse_id = fields.Many2one(comodel_name="project.estimation", string="HSE Estimation", required=False, )
    low_current_id = fields.Many2one(comodel_name="project.estimation", string="Low Current Estimation", required=False, )
    management_id = fields.Many2one(comodel_name="project.estimation", string="Management Estimation", required=False, )
    piping_id = fields.Many2one(comodel_name="project.estimation", string="Piping Estimation", required=False, )
    process_id = fields.Many2one(comodel_name="project.estimation", string="Process Estimation", required=False, )
    top_management_id = fields.Many2one(comodel_name="project.estimation", string="Top Management Estimation", required=False, )
    is_request_creator = fields.Boolean(string="Is Request Creator?", compute="_compute_is_request_creator")

    @api.depends()
    def _compute_is_request_creator(self):
        for rec in self:
            rec.is_request_creator = self.env.user.has_group('sales_team.group_sale_manager')

    @api.depends('hourly_rate', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.hourly_rate


class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    project_deliverables_id = fields.Many2one(comodel_name="project.deliverables", string="Task", required=False, )

    @api.onchange('project_deliverables_id')
    def _onchange_project_deliverables_id(self):
        if self.project_deliverables_id:
            self.name = self.project_deliverables_id.name

