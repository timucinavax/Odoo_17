# -*- coding: utf-8 -*-
{
    'name': 'Allowed Products',
    'version': '17.0.1.0.0',
    'summary': 'Allowed products in website',
    'description': 'Allowed Products',
    'category': "Sales",
    'depends': [
        'base',
        'website',
        'website_sale'
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'assets': {
        'web.assets_frontend': [
            'product_visibility/static/src/js/product_visibility.js',
        ]
    },
    'application': False,
    'license': 'LGPL-3',
}
