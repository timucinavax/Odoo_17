from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for properties of Estate'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    deadline_date = fields.Date(string="Deadline")
    validity_date = fields.Integer(string="Validity(Days)")
