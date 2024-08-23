# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductBrand(models.Model):
    """New model for product brand"""
    _name = 'product.brand'
    _description = 'Product Brand'
    _inherit = 'mail.thread'

    name = fields.Char(string="Brand", required=True)

