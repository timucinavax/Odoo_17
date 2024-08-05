# -*- coding: utf-8 -*-
from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    _name = 'material.request'
    _description = 'Material Request'
    _inherit = 'mail.thread'

    name = fields.Char(string="Name", default="New", readonly=True, copy=False)
    user_id = fields.Many2one("hr.employee", string="Employee",
                              default=lambda self: self.env.user.employee_id,
                              readonly=True, required=True)
    manager_id = fields.Many2one("hr.employee", string="Manager")
    company_id = fields.Many2one("res.company", string="Company",
                                 default=lambda self:
                                 self.env.user.company_id)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('first_approve', 'First Approved'),
        ('fully_approve', 'Fully Approved'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True, copy=False)
    date = fields.Date(string="Date", default=date.today())
    order_line_ids = fields.One2many("material.order.line",
                                     "request_id",
                                     string="Order Lines")
    is_rfq = fields.Boolean(compute="_compute_is_rfq_or_internal")
    rfq_sent = fields.Boolean(default=False, copy=False)
    is_internal = fields.Boolean(compute="_compute_is_rfq_or_internal")
    transfer_created = fields.Boolean(default=False, copy=False)
    submitted = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        res['name'] = (self.env['ir.sequence'].
                       next_by_code('material.request.sequence'))
        return res

    @api.depends('order_line_ids.type')
    def _compute_is_rfq_or_internal(self):
        # compute whether rfq and internal transfer need to be created
        self.is_rfq, self.is_internal = False, False
        for rec in self.order_line_ids:
            if 'purchase' in rec.type:
                self.is_rfq = True
            if 'internal' in rec.type:
                self.is_internal = True

    def action_create_rfq(self):
        # create rfq for product with request type purchase
        for rec in self.order_line_ids.filtered(lambda o: o.type == 'purchase'):
            sellers = rec.product_id.product_tmpl_id.seller_ids
            if not sellers:
                raise ValidationError("No vendor found for " +
                                      rec.product_id.name)
            purchase_order = (self.env['purchase.order'].search([
                                ('partner_id', '=', sellers[0].partner_id.id),
                                ('state', '=', 'draft')],
                                order='date_order desc'))
            if purchase_order:
                lines = purchase_order[0].order_line.filtered(
                    lambda o: o.product_id == rec.product_id and
                    o.request_id == self)
                if lines:
                    lines.product_qty += rec.qty
                else:
                    purchase_order[0].update({
                        'order_line': [
                            fields.Command.create({
                                'product_id': rec.product_id.id,
                                'request_id': self.id,
                                'product_qty': rec.qty,
                            })
                        ]
                    })
            else:
                self.env['purchase.order'].create({
                    'partner_id': sellers[0].partner_id.id,
                    'date_order': date.today(),
                    'order_line': [
                        fields.Command.create({
                            'product_id': rec.product_id.id,
                            'request_id': self.id,
                            'product_qty': rec.qty
                        })
                    ]
                })
            self.rfq_sent = True

    def action_create_internal(self):
        # create internal transfer for product with request type internal
        for rec in self.order_line_ids.filtered(lambda s: s.type == 'internal'):
            picking = (self.env['stock.picking'].search([
                ('request_id', '=', self.id),
                ('state', '=', 'draft')],
                order='date desc'))
            if picking:
                moves = picking.move_ids.filtered(
                    lambda m: m.product_id == rec.product_id)
                if moves:
                    moves.product_uom_qty += rec.qty
                else:
                    picking.update({
                        'move_ids': [
                            fields.Command.create({
                                'date': date.today(),
                                'product_id': rec.product_id.id,
                                'product_uom_qty': rec.qty,
                                'name': 'Internal transfer created '
                                        'from Material request',
                                'company_id': self.company_id.id,
                                'product_uom': rec.product_id.uom_id.id,
                                'procure_method': 'make_to_stock',
                                'location_id': 8,
                                'location_dest_id': 28
                            })
                        ]
                    })
            else:
                self.env['stock.picking'].create({
                    'request_id': self.id,
                    'picking_type_id': 5,
                    'location_id': 8,
                    'location_dest_id': 28,
                    'scheduled_date': datetime.now(),
                    'origin': self.name,
                    'move_ids': [
                        fields.Command.create({
                            'date': date.today(),
                            'product_id': rec.product_id.id,
                            'product_uom_qty': rec.qty,
                            'name': 'Internal transfer created '
                                    'from Material request',
                            'company_id': self.company_id.id,
                            'product_uom': rec.product_id.uom_id.id,
                            'procure_method': 'make_to_stock',
                            'location_id': 8,
                            'location_dest_id': 28
                        })
                    ]
                })
        self.transfer_created = True

    def action_submit(self):
        self.write({'state': 'submit', 'submitted': True})

    def action_first_approve(self):
        if self.env.user.has_group('material_request.material_req_head_access'):
            self.state = 'fully_approve'
        else:
            self.state = 'first_approve'

    def action_second_approve(self):
        self.state = 'fully_approve'

    def action_reject(self):
        self.state = 'rejected'


class MaterialOrderLine(models.Model):
    _name = 'material.order.line'
    _description = 'Material Order Line'

    request_id = fields.Many2one("material.request")
    sequence = fields.Char()
    product_id = fields.Many2one("product.product")
    type = fields.Selection(selection=[
        ('purchase', 'Purchase'),
        ('internal', 'Internal Transfer')
    ], required=True)
    qty = fields.Float(string="Quantity")
