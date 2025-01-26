# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectDiscipline(http.Controller):
#     @http.route('/project_discipline/project_discipline', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_discipline/project_discipline/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_discipline.listing', {
#             'root': '/project_discipline/project_discipline',
#             'objects': http.request.env['project_discipline.project_discipline'].search([]),
#         })

#     @http.route('/project_discipline/project_discipline/objects/<model("project_discipline.project_discipline"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_discipline.object', {
#             'object': obj
#         })
