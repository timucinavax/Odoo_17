# -*- coding: utf-8 -*-
from odoo import fields, models


class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _inherit = 'mail.thread'
    _description = 'Employee Transfer'

    name = fields.Char(string="Name")
    request_id = fields.Many2one("employee.transfer.request")
    employee_id = fields.Many2one("hr.employee",
                                  string="Employee",
                                  related="request_id.employee_id",)
    date = fields.Date(string="Date", related="request_id.date")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('reject', 'Rejected')
    ], default='pending', tracking=True)
    company_id = fields.Many2one("res.company",
                                 string="Current Company",
                                 related='request_id.company_id')
    dest_company_id = fields.Many2one("res.company",
                                      string="Destination Company",
                                      related='request_id.dest_company_id',)

    def action_approve(self):
        # switch the company of employee to destination company
        self.employee_id.company_id = self.dest_company_id
        self.request_id.state = 'approved'
        self.state = 'done'

    def action_reject(self):
        # reject transfer request
        self.employee_id.company_id = self.company_id
        self.request_id.state = 'reject'
        self.state = 'reject'


    def button_approve(self):
        pending_transfer = self.filtered(lambda s: s.state == 'pending')
        pending_transfer.action_approve()
