# -*- coding: utf-8 -*-
# from odoo import http


# class DiarFixPermissions(http.Controller):
#     @http.route('/diar_fix_permissions/diar_fix_permissions', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/diar_fix_permissions/diar_fix_permissions/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('diar_fix_permissions.listing', {
#             'root': '/diar_fix_permissions/diar_fix_permissions',
#             'objects': http.request.env['diar_fix_permissions.diar_fix_permissions'].search([]),
#         })

#     @http.route('/diar_fix_permissions/diar_fix_permissions/objects/<model("diar_fix_permissions.diar_fix_permissions"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('diar_fix_permissions.object', {
#             'object': obj
#         })
