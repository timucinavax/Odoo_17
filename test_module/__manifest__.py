{
    'name': 'Test Model',
    'version': '17.0.0.0.0',
    'depends': [
        'base', 'sale', 'web'
    ],
    'data': [
        # 'security/ir.model.access.cs/v',
        # 'views/test_model_views.xml',
        'views/client_views.xml'
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'test_module/static/src/xml/test_template.xml',
            'test_module/static/src/js/test.js',
            'test_module/static/src/xml/hello.xml',
            'test_module/static/src/xml/start_again.xml',
            'test_module/static/src/js/hello.js',
            'test_module/static/src/js/start_again.js',
            'test_module/static/src/xml/reset_button_temp.xml',
            'test_module/static/src/js/reset_count.js',

            # 'test_module/static/src/xml/reset_button_temp.xml',
        ]
    },
    'application': True,
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-
