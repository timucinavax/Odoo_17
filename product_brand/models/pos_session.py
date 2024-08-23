# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Load new field of existing model to pos"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('brand_id')
        return result
