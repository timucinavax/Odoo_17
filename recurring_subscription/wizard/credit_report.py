# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import date_utils
import json
import io
from psycopg2 import OperationalError
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class SubscriptionReport(models.TransientModel):
    _name = 'credit.report'
    _description = 'Credit Report'

    """ Wizard for printing report of credits with or without filter """

    subscription_ids = fields.Many2many("recurring.subscription")
    state = fields.Selection(selection=[('pending', 'Pending'),
                                        ('confirmed', 'Confirmed'),
                                        ('first_approved', 'First Approved'),
                                        ('fully_approved', 'Fully Approved'),
                                        ('rejected', 'Rejected')])

    def _get_credits(self):
        # compute credits based on selected subscriptions
        query = 'SELECT * from recurring_subscription_credit'
        params = []
        if self.subscription_ids:
            query += ' WHERE subscription_id in %s'
            params.append(tuple(self.subscription_ids.ids))
        if self.state and self.subscription_ids:
            query += ' AND state = %s'
            params.append(self.state)
        elif self.state:
            query += ' WHERE state = %s'
            params.append(self.state)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        print('get', result)
        return result

    def get_xlsx_report(self, data, response):
        # write data to xlsx file
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        main_head = workbook.add_format({'align': 'center',
                                         'bold': True,
                                         'font_size': '18px',
                                         'top': 1,
                                         'left': 1,
                                         'right': 1,
                                         'border_color': '#000000'
                                         })
        main_head.set_bg_color('#C8FFFE')
        head = workbook.add_format({'font_size': '12px',
                                    'align': 'center',
                                    'bold': True,
                                    'top': 1,
                                    'bottom': 1,
                                    'left': 1,
                                    'right': 1,
                                    'border_color': '#000000'
                                    })
        cell_format = workbook.add_format({'font_size': '10px',
                                           'align': 'center',
                                           'bottom': 1,
                                           'left': 1,
                                           'right': 1,
                                           'border_color': '#000000'})
        sheet.merge_range('A1:F2', 'Subscription Credit Report', main_head)
        sheet.set_column(1, 2, 15)
        sheet.set_column(3, 4, 20)
        sheet.write(2, 0, 'SL.No', head)
        sheet.write(2, 1, 'Subscription', head)
        sheet.write(2, 2, 'Customer', head)
        sheet.write(2, 3, 'Amount Applied', head)
        sheet.write(2, 4, 'Amount Pending', head)
        sheet.write(2, 5, 'State', head)
        row = 3
        col = 0
        for line in data:
            sheet.write(row, col, row-2, cell_format)
            sheet.write(row, col + 1, line.get('subscription_id')[1], cell_format)
            sheet.write(row, col + 2, line.get('partner_id')[1], cell_format)
            sheet.write(row, col + 3, line.get('credit_amount'), cell_format)
            sheet.write(row, col + 4, line.get('amount_pending'), cell_format)
            sheet.write(row, col + 5, dict(
                    self.subscription_ids.credit_ids._fields['state']
                    .selection).get(line.get('state')), cell_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def action_print(self):
        # create and print report in xlsx format
        result = self._get_credits()
        credit = self.subscription_ids.credit_ids
        if not credit:
            for rec in result:
                credit += self.env['recurring.subscription.credit'].browse(
                    rec['id'])
        data = credit.read()
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'credit.report',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'Credit Report',
            },
            'report_type': 'xlsx'
        }

    def action_report_credit(self):
        result = self._get_credits()
        ids = [rec.get('id') for rec in result]
        return (self.env.ref(
            'recurring_subscription.action_report_credit').report_action(ids, None))


class CreditFormReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_credit"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = False
        if self.env['recurring.subscription.credit'].search([('id', 'in', docids)]):
            docs = self.env['recurring.subscription.credit'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'data': data
        }

