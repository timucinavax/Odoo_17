from odoo import models, fields


class Specialization(models.Model):

    _name = 'hospital.specialization'
    _description = 'Specialization Categories'

    name = fields.Char(string="Specialization")