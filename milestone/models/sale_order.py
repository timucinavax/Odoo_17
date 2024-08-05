# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    milestones_count = fields.Integer(compute="_compute_milestones_count")
    update_project = fields.Boolean(default=False, copy=False)
    project_created = fields.Boolean(default=False)


    def _compute_milestones_count(self):
        # compute the count of milestone related to sale order
        for rec in self:
            rec.milestones_count = False
            if rec.project_id:
                rec.milestones_count = rec.project_id.task_ids.search_count(
                    [('project_id', '=', rec.project_id.id),
                        ('parent_id', '=', False)])

    def _link_task_and_create_subtask(self, order_line, project):
        # create task , subtask and link subtask with task
        task = project.task_ids.create({
            'name': 'Milestone ' + str(order_line.milestone)})
        project.update({
            'task_ids': [
                fields.Command.link(task.id),
                self._create_subtask(order_line, task, 0)
            ]
        })

    def _create_subtask(self, order_line, task, count):
        # create subtask and link with parent task
        return fields.Command.create({
            'name': task.name + ' - ' + order_line.product_id.name +
            ' ' + str(count + 1),
            'parent_id': task.id,
            'order_line_id': order_line.id
        })

    def action_create_project_for_product(self):
        self._create_or_update_project(False)

    def action_update_project_for_product(self):
        self._create_or_update_project('update')

    def _create_or_update_project(self, operation):
        # create or update project based on order line data
        for line in self.order_line:
            if line.milestone != 0:
                project = self.project_id
                if project:
                    # check if project exist for sale order
                    task = project.task_ids.filtered(
                        lambda t: t.name == 'Milestone ' + str(line.milestone))
                    if task:
                        # check for milestone task
                        count = project.task_ids.search_count(
                            [('parent_id', '=', task.id)])
                        sub_task = project.task_ids.filtered(
                            lambda t: t.order_line_id == line)
                        if (sub_task and sub_task.parent_id != task and
                                operation == 'update'):
                            # check for subtask with milestone name and product
                            # name
                            sub_task.parent_id = task
                            sub_task.name = (task.name + ' - ' +
                                             line.product_id.name + ' ' +
                                             str(count + 1))
                        elif not sub_task:
                            # create subtask if no subtask exist for order line
                            project.update({
                                'task_ids': [
                                    self._create_subtask(line, task, count)
                                ]
                            })
                    else:
                        # link task and create subtask
                        self._link_task_and_create_subtask(line, project)
                else:
                    # create project if no project exist for sale order
                    project = project.create({
                        'name': self.name,
                        'sale_line_id': line.order_id.id
                    })
                    self.project_id = project
                    self._link_task_and_create_subtask(line, project)
                    self.project_created = True
            else:
                # unlink task with no milestone
                if operation == 'update':
                    self.project_id.task_ids.filtered(
                        lambda t: t.order_line_id == line).unlink()
        if operation == 'update':
            # set update to False
            self.update_project = False

    def action_view_milestones(self):
        # return related projects in smart button
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'view_mode': 'kanban,form',
            'res_model': 'project.project',
            'domain': ['|', ('sale_order_id', '=', self.id),
                       ('id', 'in', self.project_ids.ids)],
            'context': "{'create': False}"
        }

    def write(self, vals):
        # enable project update button on change in order line
        if 'order_line' in vals:
            self.update_project = True
        return super().write(vals)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string="Milestone")

