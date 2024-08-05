from odoo import models, fields


class HospitalDoctor(models.Model):
    _inherit = 'hr.employee'

    specialization_ids=fields.Many2many("hospital.specialization",string="Specializations")