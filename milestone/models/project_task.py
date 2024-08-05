from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    order_line_id = fields.Many2one("sale.order.line")
