# -*- coding: utf-8 -*-
from odoo import api, models


class CreditFormReport(models.AbstractModel):
    """Get report values and returns to template"""
    _name = "report.recurring_subscription.report_credit"

    @api.model
    def _get_report_values(self, docids, data=None):
        """fetch record set form datas passed in data as report"""
        docs = self.env['recurring.subscription.credit'].browse(
            [rec['id'] for rec in data['report']])
        # returns all data to template
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
            'data': data
        }
