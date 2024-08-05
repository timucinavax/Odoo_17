# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_schedule_id = fields.Many2one("billing.schedule")
    subscription_id = fields.Many2one("recurring.subscription")
