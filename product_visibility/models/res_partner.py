from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_type = fields.Selection(selection=[('product', 'Product'),
                                               ('category', 'Category')],
                                    string="Allowed Type", required=True,
                                    default='product')
    allowed_product_ids = fields.Many2many('product.template',
                                           string="Products")
    allowed_category_ids = fields.Many2many('product.public.category',
                                            string="Categories")
