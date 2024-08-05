from odoo import models, fields, _, api


class HospitalConsultation(models.Model):
    _name = 'hospital.consultation'
    _description = 'Consultation data of a patient'
    _rec_name = 'seq_no'

    seq_no = fields.Char(string="Sequence", readonly=True, default=lambda self: _('New'))
    token_id = fields.Many2one("hospital.op.ticket", string="OP number", required=True)
    date = fields.Datetime(string="Date", required=True)
    patient_id = fields.Many2one("res.partner", string="Patient", required=True)
    doctor_id = fields.Many2one("hr.employee", string="Doctor", required=True)
    patient_age = fields.Integer(string="Patient Age")
    height = fields.Integer(string="Height")
    weight = fields.Float(string="Weight")
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
    initial_diagnosis = fields.Char(string="Initial Diagnosis")
    final_diagnosis = fields.Char(string="Final Diagnosis")
    remarks = fields.Char(string="Remarks")

    @api.model
    def create(self, vals):
        if vals.get('seq_no', _('New')) == _('New'):
            vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                'hospital.consultation') or _('New')
        res = super(HospitalConsultation, self).create(vals)
        return res

    @api.onchange('token_id')
    def _change_doctor_name(self):
        if self.token_id:
            self.doctor_id = self.token_id.doctor_id
            self.patient_id = self.token_id.patient_id
            self.patient_age = self.token_id.age
            self.date = self.token_id.date
            self.blood_group = self.token_id.blood_group
        else:
            self.doctor_id = None
            self.patient_id = None
            self.patient_age = None
            self.date = None
            self.blood_group = None

