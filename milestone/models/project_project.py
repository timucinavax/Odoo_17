# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def unlink(self):
        if self.sale_order_id:
            raise ValidationError("You can't delete a milestone project with"
                                  " a Sale Order")
        return super().unlink()
