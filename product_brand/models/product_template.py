# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    """New field for select brand from product template"""
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand')
