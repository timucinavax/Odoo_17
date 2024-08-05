from odoo import api, fields, models
import re
from odoo.exceptions import ValidationError

regex = r'^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z])(?' \
        r'=.*\d.*\d.*\d)(?=.*[^a-zA-Z0-9].' \
        r'*[^a-zA-Z0-9])[a-zA-Z\d!@#$%^&*]{8,}$'


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [
        ('unique_partner_id', 'unique(partner_account_id)',
         'A partner already exist with the same ID'),
        ('unique_establishment_id', 'unique(establishment)',
         'A Partner already exist with the same Establishment ID')
    ]

    partner_account_id = fields.Many2one("partner.account",
                                         string="Account ID")
    establishment = fields.Char(string="Establishment ID")

    @api.onchange('establishment')
    def _onchange(self):
        # validation for establishment ID
        if self.establishment:
            if not re.match(regex, self.establishment):
                raise ValidationError(
                    "Establishment ID must contain 3 alphabets,"
                    " 3 numbers and 2 special characters")

    def unlink(self):
        # remove partner id when removing partner
        self.partner_account_id.unlink()
        return super().unlink()
