# -*- coding: utf-8 -*-
# from odoo import http


# class Pagoaprod(http.Controller):
#     @http.route('/pagoaprod/pagoaprod', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pagoaprod/pagoaprod/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pagoaprod.listing', {
#             'root': '/pagoaprod/pagoaprod',
#             'objects': http.request.env['pagoaprod.pagoaprod'].search([]),
#         })

#     @http.route('/pagoaprod/pagoaprod/objects/<model("pagoaprod.pagoaprod"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pagoaprod.object', {
#             'object': obj
#         })
