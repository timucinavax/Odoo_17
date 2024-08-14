from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    product_template_id = fields.Many2one('product.template',
                                          string="Product")
    product_template_ids = fields.Many2many('product.template',
                                            string="Product",
                                            compute="_compute_product_template_ids",
                                            precompute=True)

    @api.depends('order_partner_id')
    def _compute_product_template_ids(self):
        for rec in self:
            rec.product_template_ids = rec.product_template_id.search([])
            if rec.order_partner_id.is_only_ordered:
                rec.product_template_ids = rec.product_template_ids.filtered(
                    lambda p: p.invoice_policy == 'order')
