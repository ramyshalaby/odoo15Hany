# -*- coding: utf-8 -*-
# from odoo import http


# class JournalEntryLimitAnalytical(http.Controller):
#     @http.route('/journal_entry_limit_analytical/journal_entry_limit_analytical', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/journal_entry_limit_analytical/journal_entry_limit_analytical/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('journal_entry_limit_analytical.listing', {
#             'root': '/journal_entry_limit_analytical/journal_entry_limit_analytical',
#             'objects': http.request.env['journal_entry_limit_analytical.journal_entry_limit_analytical'].search([]),
#         })

#     @http.route('/journal_entry_limit_analytical/journal_entry_limit_analytical/objects/<model("journal_entry_limit_analytical.journal_entry_limit_analytical"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('journal_entry_limit_analytical.object', {
#             'object': obj
#         })
