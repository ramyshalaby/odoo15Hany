{
    'name': 'Overtime Request',
    'version': '16.0.0.1',
    'summary': 'Request and pay employee overtime with dynamic rate',
    'description': """Request and pay employee overtime with dynamic rate for more call us on +251 969139025 or emai us on: tekleyitayew12@gmail.com """,
    'category': 'Human Resource',
    'author':'Tekle Yitayew',
    'website': '',
    'depends': [
        'hr',
        'base',
        'base_setup',
        'hr_contract'



    ],

    'license': 'LGPL-3',

    'data': [
        'security/overtime_security.xml',
        'security/ir.model.access.csv',
        'views/overtime_calculation.xml',
        'views/overtime_rate.xml',
    ],
    'assets': {},
    'installable': True,
    'application': False,
    'images': ['static/description/banner.jpg'],
}
