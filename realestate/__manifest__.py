{
    'name':'Real Estate',
    'description':'Real estate management',
    'version':'1.0',
    'depends':[

    ],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml'
    ],
    'installable': True,
    'application': True
}