# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    salesperson_id = fields.Many2one('res.users', string="Sales Person")

    def button_validate(self):
        self.salesperson_id = self.sale_id.user_id
        return super(StockPicking, self).button_validate()

