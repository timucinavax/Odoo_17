from odoo import http
from odoo.http import request


class RecurringSubscription(http.Controller):
    """ Website view of recurring subscription"""

    @http.route('/my/rec_subscription', type='http', auth="user", website=True)
    def view_recurring_subscription(self, **kwargs):
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

    @http.route('/my/rec_subscription/new', type='http', auth="user",
                website=True)
    def view_recurring_subscription(self, **kwargs):
        """View recurring subscriptions of logged user"""
        uid = request.session.uid
        print(uid)
        return request.render(
            "recurring_subscription.subscription_form")

    @http.route('/my/rec_subscription/create', type='http', auth='user',
                website=True, csrf=False)
    def recurring_subscription_create_form(self, **post):
        """Create new subscription from portal"""
        uid = request.session.uid
        print(uid)
        print(request.env['website.visitor'].
            _get_visitor_from_request().partner_id.establishment)
        record = {
            'establishment': request.env['website.visitor'].
            _get_visitor_from_request().partner_id.establishment,
            'partner_id': request.env['website.visitor'].
            _get_visitor_from_request().partner_id.id,
            'description': post.get('description'),
            'product_id': int(post.get('product_id')),
            'recurring_amount': post.get('recurring_amount')
        }
        print(record.get('establishment'))
        request.env['recurring.subscription'].create(record)
        return request.redirect('/my/rec_subscription')
