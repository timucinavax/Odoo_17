# -*- coding: utf-8 -*-
from odoo import api, models


class CreditFormReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_credit"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['recurring.subscription.credit'].browse(
            [rec['id'] for rec in data['report']])
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'data': data
        }
