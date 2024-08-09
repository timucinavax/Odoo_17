# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.tools import date_utils
from odoo.exceptions import ValidationError
import json
import io
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class CreditReport(models.TransientModel):
    """ Generate credit report in custom filters"""
    _name = 'credit.report'
    _description = 'Credit Report'

    subscription_ids = fields.Many2many("recurring.subscription")
    state = fields.Selection(selection=[('pending', 'Pending'),
                                        ('confirmed', 'Confirmed'),
                                        ('first_approved', 'First Approved'),
                                        ('fully_approved', 'Fully Approved'),
                                        ('rejected', 'Rejected')])

    def action_print_xlsx(self):
        """Create and print report in xlsx format"""
        result = self._get_credits()
        credit = self.subscription_ids.credit_ids
        if not credit:
            for rec in result:
                credit += self.env['recurring.subscription.credit'].browse(
                    rec['id'])
        data = credit.read()
        report_name = 'Credit Report'
        if len(list(self.subscription_ids)) == 1:
            report_name += ' of - ' + str(self.subscription_ids.order)
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'credit.report',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': report_name,
            },
            'report_type': 'xlsx'
        }

    def action_print_pdf(self):
        """print credit report in PDF format"""
        result = self._get_credits()
        data = {'date': self.read()[0], 'report': result}
        return (self.env.ref(
            'recurring_subscription.action_report_credit').report_action(
            None, data))

    def _get_credits(self):
        """fetch credits from database based on defined conditions"""
        query = """
        SELECT recurring_subscription_credit.id AS id,
        recurring_subscription_credit.subscription_id AS subscription_id ,
        recurring_subscription_credit.state AS state
         from recurring_subscription_credit JOIN recurring_subscription 
         ON recurring_subscription_credit.subscription_id = 
         recurring_subscription.id  AND 
         recurring_subscription.company_id in  %s
         """
        params = [tuple(self.env.company.ids)]
        if self.subscription_ids:
            query += ' AND recurring_subscription_credit.subscription_id in %s'
            params.append(tuple(self.subscription_ids.ids))
        if self.state:
            query += ' AND recurring_subscription_credit.state = %s'
            params.append(self.state)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        if not result:
            raise ValidationError("No matching records found ...!")
        return result

    def get_xlsx_report(self, data, response):
        """write data to xlsx file"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        # add format for heading,table cells etc...
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
            # write each record of data in rows
            sheet.write(row, col, row-2, cell_format)
            sheet.write(row, col + 1, line.get('subscription_id')[1],
                        cell_format)
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
