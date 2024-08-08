# -*- coding: utf-8 -*-
from datetime import timedelta, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    _name = 'recurring.subscription'
    _description = 'Recurring Subscription'
    _inherit = 'mail.thread'
    _rec_name = 'order'

    order = fields.Char(string="Order ID", default=lambda self: 'New')
    company_id = fields.Many2one("res.company", string="Company",
                                 default=lambda self:
                                 self.env.user.company_id)
    establishment = fields.Char(string="Establishment ID", required=True)
    date = fields.Date(string="Date", default=date.today())
    due_date = fields.Date(string="Due Date",
                           default=date.today() + timedelta(days=+15))
    next_billing = fields.Date(string="Next Billing")
    is_lead = fields.Boolean(string="Is Lead")
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 required=True, help="Name of the customer")
    description = fields.Char(string="Description")
    terms = fields.Html(string="Terms and Conditions")
    product_id = fields.Many2one("product.product",
                                 string="Product", required=True)
    currency_id = fields.Many2one('res.currency',
                                  string="Currency", default=lambda self: self
                                  .env.user.company_id.currency_id.id)
    recurring_amount = fields.Monetary(string="Recurring Amount")
    state = fields.Selection(string="State", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft')
    credit_ids = fields.One2many("recurring.subscription.credit",
                                 "subscription_id",
                                 string="Credit",
                                 compute="_compute_credit_ids",
                                 readonly=True)
    billing_schedule_id = fields.Many2one("billing.schedule",
                                          string="Billing Schedule")
    account_move_ids = fields.One2many("account.move",
                                       "subscription_id")
    credit_amount = fields.Monetary(store=True,
                                    compute="_compute_credit_amount")

    @api.model_create_multi
    def create(self, record):
        # sequence generation for each subscription
        rec = super(RecurringSubscription, self).create(record)
        rec['order'] = self.env['ir.sequence'].next_by_code(
            'subscription.sequence')
        return rec

    @api.depends('credit_ids')
    def _compute_credit_amount(self):
        # compute the total amount credited for the subscription
        print('compute')
        for rec in self:
            rec.credit_amount = 0.00
            rec.update({
                'credit_amount': sum(rec.credit_ids.mapped('credit_amount'))
            })

    @api.depends('due_date')
    def _compute_credit_ids(self):
        # compute related credits having end date less than due date
        for rec in self:
            rec.credit_ids = (rec.credit_ids.
                              search([('end_date', '<', rec.due_date),
                                      ('subscription_id', '=', rec.id)]))

    @api.onchange('establishment')
    def _onchange_establishment(self):
        # check for partner based on establishment id
        if self.establishment:
            self.partner_id = (self.env['res.partner'].
                               search([('establishment', '=',
                                        self.establishment)]))
            if not self.partner_id:
                raise ValidationError("No Partner found")

    def action_confirm(self):
        # move state to confirm
        self.state = 'confirm'

    def action_cancel(self):
        # move state to confirm
        self.state = 'cancel'

    @api.onchange('state')
    def send_mail(self):
        # send a mail to the customer when subscription move to done state
        if self.state == 'done':
            template = self.env.ref(
                'recurring_subscription.subscription_email_template')
            template.send_mail(self.id, force_send=True)

    def action_create_invoice(self):
        print(self)
        # create an invoice for all subscriptions which in the confirmed state
        # and due date is less than today date
        # for rec in self.search([]):
        #     if rec.due_date < date.today() and rec.state == 'confirm':
        #         rec.account_move_ids.create({
        #             'move_type': 'out_invoice',
        #             'subscription_id': rec.id,
        #             'partner_id': rec.partner_id.id,
        #             'currency_id': rec.currency_id.id,
        #             'invoice_date': date.today(),
        #             'invoice_line_ids': [
        #                 (0, 0, {
        #                     'product_id': rec.product_id.id,
        #                     'price_unit': rec.recurring_amount
        #                 })
        #             ]
        #         })
