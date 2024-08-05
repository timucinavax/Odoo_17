from odoo import models, fields, api
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Management app'

    name = fields.Char(string='Name', required=True)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Datetime(copy=False, string="Available From", default=fields.Datetime.now()+timedelta(30*3))
    expected_price = fields.Float(required=True, string='Expected Price')
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    selling_price = fields.Float(string="Sales Price", readonly='1', copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    total_area = fields.Integer(string="Total Area", compute="_compute_total")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
     ])
    active_status = fields.Boolean(string="Active")
    state_status = fields.Selection(string="Status", selection=[
        ('new', 'New'),
        ('offerreceived', 'Offer Received'),
        ('offeraccepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], default='new')
    buyer = fields.Many2one("res.partner", string="Buyer")
    seller = fields.Many2one("res.users", string="Salesman")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = []
            record.best_price = False
            for line in record['offer_ids']:
                if line.price:
                    prices.append(line.price)
                    record.best_price = max(prices)
