# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

regex = r'^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z])(?' \
        r'=.*\d.*\d.*\d)(?=.*[^a-zA-Z0-9].' \
        r'*[^a-zA-Z0-9])[a-zA-Z\d!@#$%^&*]{8,}$'


class PartnerAccount(models.Model):
    _name = 'partner.account'
    _description = 'Partner Account'
    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'A partner already exist with the same ID')
    ]

    name = fields.Char(string="Partner Account ID")

    @api.model_create_multi
    def create(self, vals):
        # partner account id validation
        res = super().create(vals)
        if not re.match(regex, vals.get('name')):
            raise ValidationError(
                "Partner Account ID must contain 3 alphabets,"
                " 3 numbers and 2 special characters")
        return res

    def write(self, vals):
        # partner account id validation
        if not re.match(regex, vals.get('name')):
            raise ValidationError(
                "Partner Account ID must contain 3 alphabets,"
                " 3 numbers and 2 special characters")
        return super().write(vals)
