from odoo import http
from odoo.exceptions import UserError
from odoo.http import request


class RecurringSubscription(http.Controller):
    """ Website view of recurring subscription"""

    @http.route('/rec-subscription', type='http', auth="user",
                website=True)
    def portal_my_rec_subscription(self, **kwargs):
        """View recurring subscriptions of logged user"""
        uid = request.session.uid
        # print(request.env['res.users'].search([('id', '=', uid)]).partner_id)
        if request.env['res.users'].search([('id', '=', uid)]).has_group(
                'base.group_portal'):
            # check whether logged user is portal user
            uid = request.env['res.users'].search([('id', '=', uid)])
            subscriptions = request.env['recurring.subscription'].sudo().search(
                [('partner_id', '=', uid.partner_id.id)])
        else:
            subscriptions = request.env['recurring.subscription'].sudo().search(
                [('create_uid', '=', uid)])
        values = {
            'record': subscriptions,
        }
        return request.render(
            "recurring_subscription.subscription_data", values)

    @http.route(
        '/rec-subscription/<model("recurring.subscription"):subscription_id>',
        type='http', auth="user",
        website=True)
    def subscription_details(self, subscription_id):
        """Detailed view of selected subscription"""
        values = {
            'subscription': subscription_id
        }
        return request.render('recurring_subscription.subscription_details',
                              values)

    @http.route('/rec-subscription/credit', type='http', auth="user",
                website=True)
    def portal_my_rec_subscription_credit(self, **kwargs):
        """View recurring subscriptions credit of logged user"""
        uid = request.session.uid
        # print(request.env['res.users'].search([('id', '=', uid)]).partner_id)
        if request.env['res.users'].search([('id', '=', uid)]).has_group(
                'base.group_portal'):
            # check whether logged user is portal user
            uid = request.env['res.users'].search([('id', '=', uid)])
            credit = request.env['recurring.subscription.credit'].sudo().search(
                [('subscription_id.partner_id', '=', uid.partner_id.id)])
        else:
            credit = request.env['recurring.subscription.credit'].sudo().search(
                [('create_uid', '=', uid)])
        values = {
            'record': credit,
        }
        return request.render(
            "recurring_subscription.credit_data", values)

    @http.route(
        '/rec-subscription/credit/<model("recurring.subscription.credit"):credit_id>',
        type='http', auth="user", website=True)
    def credit_details(self, credit_id):
        """Detailed view of recurring subscription"""
        values = {
            'credit': credit_id
        }
        return request.render('recurring_subscription.credit_details',
                              values)

    @http.route('/rec-subscription/new', type='http', auth="user",
                website=True)
    def portal_new_rec_subscription(self, **kwargs):
        """Redirect to create form for recurring subscription"""
        return request.render(
            "recurring_subscription.subscription_form")

    @http.route('/rec-subscription/credit/new', type='http', auth="user",
                website=True)
    def portal_new_rec_subscription_credit(self, **kwargs):
        """Redirect to create form for recurring subscription credit"""
        uid = request.session.uid
        return request.render(
            "recurring_subscription.credit_form")

    @http.route('/rec-subscription/create', type='http', auth='user',
                website=True, csrf=False)
    def portal_create_rec_subscription(self, **post):
        """Create new subscription from portal"""
        record = {
            'establishment': request.env['res.partner'].sudo().browse(int(post.get('partner_id'))).establishment,
            'partner_id': int(post.get('partner_id')),
            'description': post.get('description'),
            'product_id': int(post.get('product_id')),
            'date': post.get('date'),
            'due_date': post.get('due_date'),
            'recurring_amount': post.get('recurring_amount')
        }
        if not record.get('establishment'):
            raise UserError("You do not have a Establishment ID...!")
        request.env['recurring.subscription'].sudo().create(record)
        return request.redirect('/rec-subscription')

    @http.route('/rec-subscription/credit/create', type='http',
                auth='user', website=True, csrf=False)
    def portal_create_rec_subscription_credit(self, **post):
        """Create new credit from portal"""
        record = {
            'subscription_id': post.get('subscription_id'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'credit_amount': post.get('credit_amount')
        }
        request.env['recurring.subscription.credit'].sudo().create(record)
        return request.redirect('/rec-subscription/credit')

    @http.route(
        '/rec-subscription/billing-schedule/<model("recurring.subscription"):subscription_id>',
        type='http',
        auth='user', website=True, csrf=False)
    def portal_run_billing_schedule(self, subscription_id):
        """Run the billing schedule of selected subscription by managers"""
        subscription = request.env['recurring.subscription'].browse(
            subscription_id.id)
        subscription.billing_schedule_id.with_context(
            active_ids=subscription).action_create_invoices()
        return "Created invoices successfully"

    @http.route('/last_four_credits', type='json', auth='public')
    def top_selling(self):
        credit_ids = (request.env['recurring.subscription.credit'].sudo().
                      search_read(
            [('subscription_id.partner_id', '=',
              request.env.user.partner_id.id)],
            ['subscription_id', 'partner_id', 'credit_amount',
             'start_date', 'end_date', 'state'],
            limit=4, order="create_date desc"))
        return credit_ids
    