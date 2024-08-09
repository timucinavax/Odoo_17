# -*- coding: utf-8 -*-
from odoo import api, models


class SubscriptionFormReport(models.AbstractModel):
    """get report values and return to template"""
    _name = "report.recurring_subscription.report_subscription"

    @api.model
    def _get_report_values(self, docids, data=None):
        """fetch record set from datas passed in data as report"""
        docs = self.env['recurring.subscription'].browse(
            [rec['rid'] for rec in data['report']])
        # returns data and record set to template
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'data': data,
            'is_partner': data['is_partner']
        }
