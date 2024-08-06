# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from datetime import date
import json
import io
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class SubscriptionReport(models.TransientModel):
    _name = 'subscription.report'
    _description = 'Subscription Report'

    """ Wizard for print report of Subscription with given filters """
    subscription_ids = fields.Many2many("recurring.subscription")
    frequency = fields.Selection(selection=[('daily', 'Daily'),
                                            ('weekly', 'Weekly'),
                                            ('monthly', 'Monthly'),
                                            ('yearly', 'Yearly'),
                                            ('date', 'Date')])
    start_date = fields.Date()
    end_date = fields.Date()

    @api.onchange('frequency')
    def _onchange_frequency(self):
        # set the start date and end date based on selected frequency
        if self.frequency:
            self.subscription_ids = False

    @api.onchange('start_date', 'end_date')
    def _onchange_start_date(self):
        # check whether the start date is less than end date
        if (self.start_date and self.end_date and self.start_date >
                self.end_date):
            raise ValidationError("Start date must be less than end date")

    def _get_subscriptions(self):
        # get and return the subscriptions using sql query
        query = 'SELECT * from recurring_subscription'
        params = []
        if self.subscription_ids:
            query += ' WHERE id in %s'
            params.append(tuple(self.subscription_ids.ids))
        elif self.frequency:
            self.subscription_ids = False
            if self.frequency == 'daily':
                query += ' WHERE due_date = %s'
                params.append(date.today())
            elif self.frequency == 'weekly':
                query += (' WHERE EXTRACT(WEEK from due_date) ='
                          ' EXTRACT(WEEK from CURRENT_DATE)')
            elif self.frequency == 'monthly':
                query += (' WHERE EXTRACT(MONTH from due_date) ='
                          ' EXTRACT(MONTH from CURRENT_DATE)')
            elif self.frequency == 'yearly':
                query += (' WHERE EXTRACT(YEAR from due_date) ='
                          ' EXTRACT(YEAR from CURRENT_DATE)')
            elif self.frequency == 'date':
                if self.start_date and not self.end_date:
                    query += ' WHERE due_date >= %s'
                    params.append(self.start_date)
                elif self.end_date and not self.start_date:
                    query += ' WHERE due_date <= %s'
                    params.append(self.end_date)
                elif self.start_date and self.end_date:
                    query += ' WHERE due_date BETWEEN %s and %s'
                    params.append(self.start_date)
                    params.append(self.end_date)
        self.env.cr.execute(query, tuple(params))
        result = self.env.cr.dictfetchall()
        if not result:
            raise ValidationError("No matching records found...!")
        return result

    def action_print_pdf(self):
        # print report in PDF format
        result = self._get_subscriptions()
        data = {'date': self.read()[0], 'report': result}
        return (self.env.ref(
            'recurring_subscription.action_report_subscription').report_action(
            None, data))

    def action_print_xlsx(self):
        # print report in xlsx format
        result = self._get_subscriptions()
        subscription = self.subscription_ids
        if not subscription:
            for rec in result:
                subscription += self.subscription_ids.browse(rec['id'])
        data = subscription.read()
        report_name = 'Subscription Report'
        if len(subscription) == 1:
            report_name += ' of - ' + str(subscription.order)
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'subscription.report',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': report_name,
            },
            'report_type': 'xlsx'
        }

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
                                         'border_color': '#000000'})
        main_head.set_bg_color('#C8FFFE')
        head = workbook.add_format({'font_size': '12px',
                                    'align': 'center',
                                    'bold': True,
                                    'top': 1,
                                    'bottom': 1,
                                    'left': 1,
                                    'right': 1,
                                    'border_color': '#000000'})
        cell_format = workbook.add_format({'font_size': '10px',
                                           'align': 'center',
                                           'bottom': 1,
                                           'left': 1,
                                           'right': 1,
                                           'border_color': '#000000'})
        sheet.merge_range('A1:G2', 'Subscription Report', main_head)
        sheet.set_column(1, 2, 15)
        sheet.set_column(3, 3, 20)
        sheet.set_column(5, 5, 20)
        sheet.write(2, 0, 'SL.No', head)
        sheet.write(2, 1, 'Name', head)
        sheet.write(2, 2, 'Customer', head)
        sheet.write(2, 3, 'Product', head)
        sheet.write(2, 4, 'Amount', head)
        sheet.write(2, 5, 'Total Credit Applied', head)
        sheet.write(2, 6, 'State', head)
        row = 3
        col = 0
        for line in data:
            sheet.write(row, col, row-2, cell_format)
            sheet.write(row, col + 1, line.get('order'), cell_format)
            sheet.write(row, col + 2, line.get('partner_id')[1], cell_format)
            sheet.write(row, col + 3, line.get('product_id')[1], cell_format)
            sheet.write(row, col + 4, line.get('recurring_amount'), cell_format)
            sheet.write(row, col + 5, line.get('credit_amount'), cell_format)
            sheet.write(row, col + 6, dict(self.subscription_ids.
                                           _fields['state'].selection).get(
                line.get('state')), cell_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
