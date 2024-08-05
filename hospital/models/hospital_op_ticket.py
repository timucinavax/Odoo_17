from odoo import models, fields, api, _
from datetime import datetime


class HospitalOpTicket(models.Model):
    _name = 'hospital.op.ticket'
    _description = 'Manage op tickets'
    _rec_name = 'op_number'

    token_no = fields.Char(string='Token No', readonly=True, default=lambda self: _('New'))
    op_number = fields.Char(string="OP Number", required=True, default=lambda self: _('New'))
    patient_id = fields.Many2one("res.partner", string="Patient Name", required=True)
    doctor_id = fields.Many2one("hr.employee", string="Consulting Doctor", required=True)
    date = fields.Datetime(string="Date", required=True, default=datetime.now())
    age = fields.Integer(string="Age")
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
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female')])
    fee = fields.Float(string="Fees")

    @api.model
    def create(self, vals):
        print(vals)
        doctor = vals.get('doctor_id')
        user = self.env['ir.sequence'].search([('x_user_id', '=', 'doctor')])
        print(user)
        if vals.get('token_no', _('New')) == _('New'):
            vals['token_no'] = self.env['ir.sequence'].next_by_code(
                'hospital.op.ticket') or _('New')
            vals['op_number'] = self.env['ir.sequence'].next_by_code(
                'hospital.op.token') or _('New')
        res = super(HospitalOpTicket, self).create(vals)
        return res

    @api.onchange('patient_id')
    def _change_patient(self):
        if self.patient_id:
            self.age = self.patient_id.age
            self.blood_group = self.patient_id.blood_group
            self.gender = self.patient_id.gender
        else:
            self.age = None
            self.blood_group = None
            self.gender = None

    @api.onchange('doctor_id')
    def _change_doctor(self):
        if self.doctor_id:
            self.fee = self.doctor_id.hourly_cost
        else:
            self.fee = None
