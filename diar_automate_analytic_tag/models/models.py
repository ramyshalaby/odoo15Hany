# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID


class Project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    @api.model
    def create(self, values):
        res = super(Project, self).create(values)
        # The following lines will get the created analytic account and use it to create analytic tag
        analytic_account_id = res.analytic_account_id
        analytic_tag_obj = self.env['account.analytic.tag'].create({'name': analytic_account_id.name,
                                                                    'active_analytic_distribution': True})
        self.env['account.analytic.distribution'].create({'account_id': analytic_account_id.id, 'percentage': 100.0, 'tag_id': analytic_tag_obj.id})
        return res


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    diar_analytic_tag_id = fields.Many2one(comodel_name="account.analytic.tag", string="Analytic Tag", required=False, )

    @api.onchange('diar_analytic_tag_id')
    def _onchange_diar_analytic_tag_id(self):
        if self.diar_analytic_tag_id:
            return {'value': {'analytic_tag_ids': [(6, 0, [self.diar_analytic_tag_id.id])]}}
        else:
            return {'value': {'analytic_tag_ids': [(6, 0, [])]}}


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    allowed_analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", relation="account_move_account_analytic_tag_rel", column1="move_id", column2="tag_id", string="Allowed Tags")

    @api.onchange('partner_id')
    def _compute_allowed_analytic_tag_ids(self):
        env_analytic_tag = self.env['account.analytic.tag'].with_user(SUPERUSER_ID)
        if self.partner_id:
            tag_objs = env_analytic_tag.search([('related_partner_id', '=', self.partner_id.id)])
            return {'value': {'allowed_analytic_tag_ids': [(6, 0, tag_objs.ids)]}}


class AccountAnalyticTag(models.Model):
    _name = 'account.analytic.tag'
    _inherit = 'account.analytic.tag'

    related_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", compute="_compute_related_partner_id", store=True)

    @api.depends('analytic_distribution_ids')
    def _compute_related_partner_id(self):
        for rec in self:
            if rec.analytic_distribution_ids:
                rec.related_partner_id = rec.analytic_distribution_ids[0].account_id.partner_id.id
