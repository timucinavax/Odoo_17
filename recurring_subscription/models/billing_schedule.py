# -*- coding: utf-8 -*-
from datetime import date
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _inherit = 'mail.thread'

    name = fields.Char(string="Name")
    simulation = fields.Boolean(string="Simulation")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    partner_ids = fields.Many2many("res.partner",
                                   string="Customer")
    credit_amount = fields.Monetary(string="Total Credit Amount",
                                    compute="_compute_credit_amount")
    currency_id = fields.Many2one("res.currency",
                                  string="Currency",
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id)
    active = fields.Boolean(string="Active", default=True)
    subscription_ids = fields.One2many("recurring.subscription",
                                       "billing_schedule_id",
                                       string="Subscriptions",
                                       readonly=True)
    subscription_count = fields.Integer(compute='_compute_subscription_count')
    credit_ids = fields.One2many("recurring.subscription.credit",
                                 "billing_schedule_id",
                                 string="Credits",
                                 readonly=True)
    invoice_ids = fields.One2many("account.move",
                                  "billing_schedule_id",
                                  string="Invoices")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.depends('subscription_count')
    def _compute_subscription_count(self):
        # compute total related subscription count
        for rec in self:
            rec.subscription_count = len(rec.subscription_ids.ids)

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        # compute total related invoice count
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids.ids)

    @api.depends('credit_amount')
    def _compute_credit_amount(self):
        # compute credit amount based on billing schedule and state in confirm
        for rec in self:
            rec.credit_amount = sum(rec.credit_ids.search([
                ('subscription_id.state',
                 '=', 'confirm'),
                ('subscription_id.billing_schedule_id', '=', rec.id)]).mapped(
                'credit_amount'))

    @api.onchange('start_date', 'end_date')
    def _onchange_start_date(self):
        # check whether the start date is less than end date or not
        if (self.start_date and self.end_date and self.start_date >
                self.end_date):
            raise ValidationError("Start date must be less than end date")

    def action_view_subscription(self):
        # return related subscriptions
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'view_mode': 'tree,form',
            'res_model': 'recurring.subscription',
            'domain': [('id', 'in', self.subscription_ids.ids)],
            'context': "{'create': False}"
        }

    def action_create_invoices(self):
        # create invoice with credits
        for rec in self.subscription_ids:
            self.invoice_ids.create({
                'move_type': 'out_invoice',
                'subscription_id': rec.id,
                'billing_schedule_id': self.id,
                'partner_id': rec.partner_id.id,
                'currency_id': rec.currency_id.id,
                'invoice_date': date.today(),
                'invoice_line_ids': [
                    fields.Command.create({
                        'product_id': rec.product_id.id,
                        'price_unit': rec.recurring_amount
                    })
                ],
            })
            total_credit = 0
            for line in rec.credit_ids:
                total_credit += line.credit_amount
                if rec.recurring_amount in rec.credit_ids.mapped(
                        'credit_amount'):
                    self._add_credit(-rec.recurring_amount, rec, line)
                    break
                elif (line.credit_amount <= rec.recurring_amount and
                      total_credit <= rec.recurring_amount):
                    self._add_credit(-line.credit_amount, rec, line)
        self.active = False

    def _add_credit(self, val, record, line):
        # add credits to related subscription invoice
        record.account_move_ids.invoice_line_ids = [
            fields.Command.create({
                'name': line.name,
                'price_unit': val
            })
        ]

    def action_view_invoice(self):
        # return created invoices
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('billing_schedule_id', '=', self.id)],
            'context': "{'create': False}"
        }
