# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    request_id = fields.Many2one("material.request",
                                 string="Material Request")

