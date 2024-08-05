{
    'name':'Hospital',
    'description':'Hospital management module',
    'version':'1.0',
    'depends':[
        'hr',
        'base',
        'hr_hourly_cost'
    ],
    'data':[
        'views/hospital_patient_views.xml',
        'views/hospital_doctor_views.xml',
        'views/hospital_specialization_views.xml',
        'views/hospital_op_ticket_views.xml',
        'views/hospital_consultation_views.xml',
        'views/hospital_medicine_views.xml',
        'security/ir.model.access.csv',
        'data/hospital_op_ticket_sequence.xml',
        'data/hospital_consultation_sequence.xml'
    ],
    'installable': True,
    'application': True

}