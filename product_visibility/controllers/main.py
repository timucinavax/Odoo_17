# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ProductVisibility(http.Controller):
    @http.route('/get_allowed_products', auth='user', type='json', website=True)
    def get_allowed_products(self):
        domain = []
        if request.env.user.has_group('base.group_portal'):
            if request.env.user.partner_id.allowed_type == 'product':
                domain = [('id', 'in', request.env.user.partner_id.
                           allowed_product_ids.ids)]
            elif request.env.user.partner_id.allowed_type == 'category':
                domain = [('categ_id', 'in', request.env.user.partner_id.
                           allowed_category_ids.ids)]
        products = request.env['product.template'].sudo().search(domain)
        return products
