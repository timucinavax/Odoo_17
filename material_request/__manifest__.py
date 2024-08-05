# -*- coding: utf-8 -*-
{
    'name': 'Material Request',
    'version': '17.0.1.0.0',
    'summary': 'Module for Material Request',
    'description': 'Material Request',
    'category': "Sales",
    'depends': [
        'base',
        'mail',
        'sale',
        'purchase',
        'stock',
        'hr'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'data/ir_sequence_data.xml',
        'views/material_request_views.xml',
        'views/purchase_order_line_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
