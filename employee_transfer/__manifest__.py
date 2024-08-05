# -*- coding: utf-8 -*-
{
    'name': 'Employee Transfer',
    'version': '17.0.1.0.0',
    'summary': 'Module for Employee Transfer',
    'description': 'Employee Transfer from one company to another',
    'category': "Human Resources",
    'depends': [
        'base',
        'hr',
        'mail'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'data/ir_sequence_data.xml',
        'views/employee_transfer_request_views.xml',
        'views/employee_transfer_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
