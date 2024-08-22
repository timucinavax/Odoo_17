from odoo import fields, models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('product.template')
        return result

    def _loader_params_product_template(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['brand_id']
            }
        }
        return result

    def _get_pos_ui_product_template(self, params):
        return self.env['product.template'].search_read(**params['search_params'])


