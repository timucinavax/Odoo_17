# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class EmployeeTransferRequest(models.Model):
    _name = 'employee.transfer.request'
    _inherit = 'mail.thread'
    _description = 'Employee Transfer Request'

    name = fields.Char(string='Name', default='New', readonly=True)
    user_id = fields.Many2one("res.users", string="User",
                              default=lambda self: self.env.user)
    user_ids = fields.Many2many("res.users", compute='_compute_user_ids')
    employee_id = fields.Many2one("hr.employee", string="Employee",
                                  required=True)
    company_id = fields.Many2one("res.company", string="Current Company",
                                 compute="_compute_company_id")
    date = fields.Date(string="Date", default=fields.Date.today())
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approved', 'Approved'),
        ('reject', 'Rejected')
    ], default='draft', tracking=True)
    dest_company_id = fields.Many2one("res.company",
                                      string="Destination Company",
                                      required=True)
    transfer_id = fields.Many2one("employee.transfer")

    @api.depends('employee_id')
    def _compute_company_id(self):
        # compute current company based on selected employee
        for record in self:
            record.company_id = False
            if record.employee_id:
                record.company_id = record.employee_id.company_id

    @api.depends('user_id')
    def _compute_user_ids(self):
        # compute the dynamic domain field for employee user
        for record in self:
            record.user_ids = False
            if not record.user_ids:
                record.user_ids = self.env.ref(
                    'employee_transfer.employee_transfer_manager_access').users

    @api.model_create_multi
    def create(self, vals):
        # create request with sequence and validate company
        res = super().create(vals)
        res['name'] = (self.env['ir.sequence'].
                       next_by_code('employee.transfer.sequence'))
        if res['company_id'] == res['dest_company_id']:
            raise ValidationError(
                "Current and Destination company cannot be same...!")
        return res

    def action_submit(self):
        # create a transfer when submit the request
        self.transfer_id = self.transfer_id.create({
            'name': 'Transfer request from ' + self.employee_id.name + ' to ' + self.dest_company_id.name + ' on ' + str(self.date),
            'request_id': self.id
        })
        self.state = 'submit'
