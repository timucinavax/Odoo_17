# -*- coding: utf-8 -*-
from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def _search_exact(self, search_details, search, limit, order):
        """Overwrite existing function of returning search result to website"""
        all_results = []
        total_count = 0
        for search_detail in search_details:
            model = self.env[search_detail['model']]
            results, count = model._search_fetch(search_detail, search, limit,
                                                 order)
            if self.env.user.has_group('base.group_portal'):
                # check whether logged user is a portal user
                if (self.env.user.partner_id.allowed_type == 'product' and
                        model == self.env['product.template']):
                    # check whether logged user allowed type is porduct
                    results = results.filtered(
                        lambda p: p.id in self.env.user.partner_id.
                        allowed_product_ids.ids)
                elif self.env.user.partner_id.allowed_type == 'category':
                    # check whether logged user allowed type is category
                    if model == self.env['product.public.category']:
                        # filter categories to allowed categories
                        results = results.filtered(
                            lambda c: c.id in self.env.user.partner_id.
                            allowed_category_ids.ids)
                    elif model == self.env['product.template']:
                        # filter products to allowed products
                        results = results.filtered(
                            lambda p: any(
                                pid in p.public_categ_ids.ids for pid in
                                self.env.
                                user.partner_id.allowed_category_ids.ids))
            search_detail['results'] = results
            total_count += count
            search_detail['count'] = count
            all_results.append(search_detail)
        return total_count, all_results
