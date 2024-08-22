# -*- coding: utf-8 -*-
{
    'name': 'Product Brand',
    'version': '17.0.1.0.0',
    'summary': 'Product Brand',
    'description': 'Product Brand',
    'category': "Sales",
    'depends': [
        'base',
        'point_of_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_brand_views.xml',
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'product_brand/static/src/**/*',
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
