# -*- coding: utf-8 -*-
{
    'name': 'Session Discount',
    'version': '17.0.1.0.0',
    'summary': 'Session discount',
    'description': 'Session discount',
    'category': "Sales",
    'depends': [
        'base',
        'point_of_sale'
    ],
    'data': [
        # 'views/ir_config_settings_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'session_discount/static/src/**/*',
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
