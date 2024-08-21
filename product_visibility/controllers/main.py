# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class ProductVisibility(WebsiteSale):
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """Override existing function to show only allowed product and
         categories to customer on website"""
        res = super().shop(
            page, category, search, min_price, max_price, ppg, **post)
        product_domain = []
        cate_domain = []
        if request.env.user.has_group('base.group_portal'):
            # check whether the logged user is a portal user
            if request.env.user.partner_id.allowed_type == 'category':
                # check whether logged customer has allowed type category
                cate_domain = [('id', 'in', request.env.user.partner_id.
                                allowed_category_ids.ids)]
                product_domain = [('public_categ_ids', 'in', request.env.user.
                                   partner_id.allowed_category_ids.ids)]
            elif request.env.user.partner_id.allowed_type == 'product':
                # check whether logged customer has allowed type product
                product_domain = [('id', 'in', request.env.user.partner_id.
                                   allowed_product_ids.ids)]
        products = request.env['product.template'].sudo().search(product_domain)
        categories = request.env['product.public.category'].sudo().search(
            cate_domain)
        # return allowed products and categories
        res.qcontext['products'] = products
        res.qcontext['categories'] = categories
        return res
