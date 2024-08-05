from odoo import api, fields, models


class TestModel(models.Model):
    _name = 'test.model'

    name = fields.Char()
    tag_ids = fields.Many2many('res.partner.category')
    line_ids = fields.One2many("test.model.line", "model_id")

    def action_add(self):
        # print(self.line_ids)
        # value4 = self.tag_ids.filtered(lambda r:  r.name == 'cybro').id
        value4 = self.tag_ids.search([('name', '=', 'cybro')])
        print(value4)
        # value = self.tag_ids.search([('name', '=', 'Employees')],limit=1)
        value2 = self.env.ref('base.res_partner_category_11')
        value = self.env.ref('base.res_partner_category_3')
        value1 = self.env.ref('base.res_partner_category_8')
        # values = self.line_ids.search([('name', '=', 'rec 3'),('model_id', '=', self.id)])
        # print('h', values)
        # print(value)
        # self.tag_ids = [fields.Command.set(value4.ids)]
        # print(self.env.user.name)
        # partner = self.env['res.partner'].create({
        #     'name': "abd"
        # })
        # self.env['res.users'].create({
        #     'login': 'ghj',
        #     'partner_id': partner.id
        # })







        # value.unlink()
        # self.env['test.model.line'].create({
        #     'name': 'rec 2',
        #     'model_id': self.id
        # })
        # self.write({
        #     'line_ids': [
        #         fields.Command.update(value.id, {'name': 'record'})
        #     ]
        # })

class TestModelLine(models.Model):
    _name = 'test.model.line'

    model_id = fields.Many2one("test.model")
    name = fields.Char()



