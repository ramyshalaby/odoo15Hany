# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'
    
    default_analytic_account_ids = fields.Many2many(comodel_name="account.analytic.account", relation="move_line_defaults_rel", column1="move_line_id", column2="default_analytic_account_id", string="Default Analytic Account")

    @api.onchange('account_id')
    def _compute_default_analytic_account(self):
        selected_account = self._context.get('selected_account')

        if selected_account and self.account_id:
            default_analytic_accounts = self.env['account.analytic.default'].search(
                [('account_id', '=', self.account_id.id)])
            allowed_analytic_accounts = []
            for analytic_account in default_analytic_accounts:
                allowed_analytic_accounts.append(analytic_account.analytic_id.id)

            if allowed_analytic_accounts:
                return {'value': {'default_analytic_account_ids': [(6, 0, allowed_analytic_accounts)]}}
            else:
                return {'value': {'default_analytic_account_ids': [(6, 0, [])]}}

