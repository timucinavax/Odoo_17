# -*- coding: utf-8 -*-
{
    'name': 'Confirm Sale Order',
    'version': '17.0.1.0.0',
    'summary': 'Module for Corfirm Sale Order',
    'description': 'Sale Order Confirmation',
    'category': "Sales",
    'depends': [
        'base',
        'sale',
        'stock'
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
