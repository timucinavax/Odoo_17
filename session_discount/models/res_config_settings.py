from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_session_discount = fields.Boolean()
    session_discount = fields.Float()