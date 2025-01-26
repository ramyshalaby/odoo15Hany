# -*- coding: utf-8 -*-
# from odoo import http


# class DiarAutomateAnalyticTag(http.Controller):
#     @http.route('/diar_automate_analytic_tag/diar_automate_analytic_tag', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/diar_automate_analytic_tag/diar_automate_analytic_tag/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('diar_automate_analytic_tag.listing', {
#             'root': '/diar_automate_analytic_tag/diar_automate_analytic_tag',
#             'objects': http.request.env['diar_automate_analytic_tag.diar_automate_analytic_tag'].search([]),
#         })

#     @http.route('/diar_automate_analytic_tag/diar_automate_analytic_tag/objects/<model("diar_automate_analytic_tag.diar_automate_analytic_tag"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('diar_automate_analytic_tag.object', {
#             'object': obj
#         })
