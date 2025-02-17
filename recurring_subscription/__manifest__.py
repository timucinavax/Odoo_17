# -*- coding: utf-8 -*-
{
    'name': 'Recurring Subscription',
    'version': '17.0.5.0.0',
    'summary': 'Module for Recurring Subscription',
    'description': 'Recurring Subscription',
    'category': "Sales",
    'depends': [
        'base',
        'crm',
        'sale',
        'account',
        'web',
        'website'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'data/product_data.xml',
        'data/ir_sequence_data.xml',
        'data/subscription_email_template.xml',
        'data/ir_cron_data.xml',
        'report/report_templates.xml',
        'report/ir_actions_report.xml',
        'views/recurring_subsription_templates.xml',
        'views/recurring_subscription_credit_templates.xml',
        'views/snippet.xml',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/recurring_subscription_views.xml',
        'views/recurring_subscription_credit_views.xml',
        'views/billing_schedule_views.xml',
        'views/account_move_views.xml',
        'wizard/subscription_report_views.xml',
        'wizard/credit_report_views.xml',
        'views/recurring_subscription_menuitem.xml'
    ],
    'installable': True,
    'assets':{
        'web.assets_backend':[
            'recurring_subscription/static/src/js/action_manager.js'
        ],
        'web.assets_frontend':[
            'recurring_subscription/static/src/js/recurring_subscription.js',
            'recurring_subscription/static/src/xml/recurring_subscription_snippet_templates.xml',
        ]
    },
    'application': True,
    'license': 'LGPL-3',
}





