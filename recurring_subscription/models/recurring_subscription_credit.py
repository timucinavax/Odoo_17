# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RecurringSubscriptionCredit(models.Model):
    _name = 'recurring.subscription.credit'
    _description = 'Recurring Subscription Credit'
    _inherit = 'mail.thread'

    name = fields.Char(string="Name")
    subscription_id = fields.Many2one("recurring.subscription",
                                      string="Subscription", required=True)
    company_id = fields.Many2one("res.company", string="Company",
                                 related="subscription_id.company_id")
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 related="subscription_id.partner_id")
    establishment = fields.Char(string="Establishment ID",
                                related="subscription_id.establishment")
    due_date = fields.Date(string="Due Date",
                           related="subscription_id.due_date")
    currency_id = fields.Many2one('res.currency',
                                  string="Currency", default=lambda self: self
                                  .env.user.company_id.currency_id.id)
    credit_amount = fields.Monetary(string="Credit amount")
    product_id = fields.Many2one('product.product',
                                 related="subscription_id.product_id")
    product_image = fields.Binary(related="subscription_id.product_image")
    state = fields.Selection(string="State", selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('first_approved', 'First Approved'),
        ('fully_approved', 'Fully Approved'),
        ('rejected', 'Rejected')
    ], default="pending")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    billing_schedule_id = fields.Many2one("billing.schedule",
                                          related="subscription_id."
                                                  "billing_schedule_id")
    amount_pending = fields.Monetary(compute="_compute_amount_pending")

    @api.onchange('start_date', 'end_date')
    def _onchange_start_date(self):
        # check whether the start date is less than end date
        if (self.start_date and self.end_date and self.start_date >
                self.end_date):
            raise ValidationError("Start date must be less than end date")

    @api.onchange('credit_amount')
    def _onchange_amount(self):
        # check for whether the subscription match with credit amount
        if (self.credit_amount == 0.00 or
                self.credit_amount > self.subscription_id.recurring_amount):
            self.subscription_id = None

    @api.depends('credit_amount')
    def _compute_amount_pending(self):
        # compute pending credit amount of subscription
        for record in self:
            record.amount_pending = False
            record.amount_pending = (record.subscription_id.recurring_amount -
                                     record.subscription_id.credit_amount)
