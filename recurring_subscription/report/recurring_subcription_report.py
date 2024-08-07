# -*- coding: utf-8 -*-
from odoo import api, models


class SubscriptionFormReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_subscription"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['recurring.subscription'].browse(
            [rec['id'] for rec in data['report']])
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'data': data,
            'is_partner': data['is_partner']
        }
