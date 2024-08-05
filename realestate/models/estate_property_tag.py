from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for estate properties'

    tag_id = fields.Char(string="Tag", required=True)
