from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def _search_exact(self, search_details, search, limit, order):
        res = super()._search_exact(search_details, search, limit, order)
        print(self.read())
        domain = ["&", "&", ("sale_ok", "=", True),
                  ("website_id", "in", (False, self.id)),
                  ("is_published", "=", True)]
        if self.env.user.has_group('base.group_portal'):
            domain.insert(0, "&")
            if self.env.user.partner_id.allowed_type == 'product':
                domain.append(("id", "in",
                              self.env.user.partner_id.allowed_product_ids.ids))
            elif self.env.user.partner_id.allowed_type == 'category':
                domain.append(("public_categ_ids",
                              "in", self.env.user.partner_id.allowed_category_ids.ids))
        print(domain)
        print(res[1][0]['base_domain'][0])
        return res