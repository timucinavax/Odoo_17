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
            subscriptions = request.env['recurring.subscription'].search(
                [('create_uid', '=', uid)])
        values = {
            'record': subscriptions,
        }
        return request.render(
            "recurring_subscription.subscription_data", values)

    @http.route('/rec-subscription/credit', type='http', auth="user",
                website=True)
    def portal_my_rec_subscription_credit(self, **kwargs):
        """View recurring subscriptions of logged user"""
        uid = request.session.uid
        # print(request.env['res.users'].search([('id', '=', uid)]).partner_id)
        if request.env['res.users'].search([('id', '=', uid)]).has_group(
                'base.group_portal'):
            # check whether logged user is portal user
            uid = request.env['res.users'].search([('id', '=', uid)])
            credit = request.env['recurring.subscription.credit'].sudo().search(
                [('subscription_id.partner_id', '=', uid.partner_id.id)])
        else:
            credit = request.env['recurring.subscription.credit'].search(
                [('create_uid', '=', uid)])
        values = {
            'record': credit,
        }
        return request.render(
            "recurring_subscription.credit_data", values)

    @http.route('/rec-subscription/new', type='http', auth="user",
                website=True)
    def portal_new_rec_subscription(self, **kwargs):
        """View recurring subscriptions of logged user"""
        uid = request.session.uid
        return request.render(
            "recurring_subscription.subscription_form")

    @http.route('/rec-subscription/credit/new', type='http', auth="user",
                website=True)
    def portal_new_rec_subscription_credit(self, **kwargs):
        """View recurring subscriptions of logged user"""
        uid = request.session.uid
        return request.render(
            "recurring_subscription.credit_form")

    @http.route('/rec-subscription/create', type='http', auth='user',
                website=True, csrf=False)
    def portal_create_rec_subscription(self, **post):
        """Create new subscription from portal"""
        print(post.get('product_id'))
        uid = request.session.uid
        partner = request.env['res.users'].search([('id', '=', uid)]).partner_id
        record = {
            'establishment': partner.establishment,
            'partner_id': partner.id,
            'description': post.get('description'),
            'product_id': int(post.get('product_id')),
            # 'recurring_amount': post.get('recurring_amount')
        }
        if not record.get('establishment'):
            raise UserError("You do not have a Establishment ID...!")
        request.env['recurring.subscription'].sudo().create(record)
        return request.redirect('/rec-subscription')

    @http.route('/rec-subscription/credit/create', type='http',
                auth='user', website=True, csrf=False)
    def portal_create_rec_subscription_credit(self, **post):
        """Create new subscription from portal"""
        record = {
            'subscription_id': post.get('subscription_id'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'credit_amount': post.get('credit_amount')
        }
        request.env['recurring.subscription.credit'].sudo().create(record)
        return request.redirect('/rec-subscription/credit')
