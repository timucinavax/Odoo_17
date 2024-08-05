# -*- coding: utf-8 -*-
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _sql_constraints = [
        ('unique_order', 'unique(order)',
         'A Lead already exist with the same Order ID')
    ]

    order = fields.Char(string="Order ID", required=True)
