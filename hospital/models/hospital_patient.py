from odoo import models, fields


class HospitalPatient(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(string="Age")
    dob = fields.Date(string="Date of Birth")
    blood_group = fields.Selection(string="Blood Group", selection=[
        ('a+ve', 'A+ve'),
        ('b+ve', 'B+ve'),
        ('ab+ve', 'AB+ve'),
        ('o+ve', 'O+ve'),
        ('a-ve', 'A-ve'),
        ('b-ve', 'B-ve'),
        ('ab-ve', 'AB-ve'),
        ('o-ve', 'O-ve')
    ])
    sequence = fields.Char(string="Sequence")
    gender = fields.Selection(string="Gender",selection=[
        ('male', 'Male'),
        ('female', 'Female')
    ])
