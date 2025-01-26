# -*- coding: utf-8 -*-
# from odoo import http


# class DiarTasksCostReport(http.Controller):
#     @http.route('/diar_tasks_cost_report/diar_tasks_cost_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/diar_tasks_cost_report/diar_tasks_cost_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('diar_tasks_cost_report.listing', {
#             'root': '/diar_tasks_cost_report/diar_tasks_cost_report',
#             'objects': http.request.env['diar_tasks_cost_report.diar_tasks_cost_report'].search([]),
#         })

#     @http.route('/diar_tasks_cost_report/diar_tasks_cost_report/objects/<model("diar_tasks_cost_report.diar_tasks_cost_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('diar_tasks_cost_report.object', {
#             'object': obj
#         })
