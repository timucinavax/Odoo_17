# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _name = 'confirm.sale.order'
    _description = 'Sale Order'

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    state_id = fields.Selection(string="State", related='sale_order_id.state')

    def action_confirm(self):
        self.sale_order_id.state = 'sale'
        print(self.sale_order_id.state)
