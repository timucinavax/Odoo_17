from odoo import fields, models


class PosSession(models.Model):
    _inherit = 'pos.order.line'

    brand_id = fields.Many2one('product.brand',
                               related='product_id.product_tmpl_id.brand_id')
