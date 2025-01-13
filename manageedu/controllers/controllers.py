# -*- coding: utf-8 -*-
# from odoo import http


# class Manageedu(http.Controller):
#     @http.route('/manageedu/manageedu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manageedu/manageedu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manageedu.listing', {
#             'root': '/manageedu/manageedu',
#             'objects': http.request.env['manageedu.manageedu'].search([]),
#         })

#     @http.route('/manageedu/manageedu/objects/<model("manageedu.manageedu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manageedu.object', {
#             'object': obj
#         })
