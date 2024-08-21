# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website
from odoo import http
from odoo.http import request


class ProductVisibility(WebsiteSale):

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        res = super()._shop_lookup_products(attrib_set, options, post, search, website)
        domain = []
        if request.env.user.has_group('base.group_portal'):
            if request.env.user.partner_id.allowed_type == 'product':
                domain = [('id', 'in', request.env.user.partner_id.
                           allowed_product_ids.ids)]
            elif request.env.user.partner_id.allowed_type == 'category':
                domain = [('public_categ_ids', 'in', request.env.user.partner_id.
                           allowed_category_ids.ids)]
        products = request.env['product.template'].sudo().search(domain)
        res = list(res)
        res[2] = products
        return tuple(res)

    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super().shop(page, category, search, min_price, max_price, ppg, **post)
        domain = []
        if request.env.user.has_group('base.group_portal'):
            if request.env.user.partner_id.allowed_type == 'category':
                domain = [('id', 'in', request.env.user.partner_id.
                           allowed_category_ids.ids)]
        categories = request.env['product.public.category'].sudo().search(domain)
        res.qcontext['categories'] = categories
        return res
class SearchProductVisibility(Website):
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        res = super().autocomplete(search_type, term, order, limit, max_nb_chars, options)
        print(res)
        return res