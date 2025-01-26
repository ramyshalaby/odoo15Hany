# -*- encoding: utf-8 -*-
{
    "name": "ODOO Warehouse and Journal User restriction",
    "version": "1.0.0",
    "category": "stock, account",
    'author': 'Mohamed Mtloob',
    'website': 'https://www.linkedin.com/in/mohamed-mtloob-62b33b76/',
    'license': 'OPL-1',
    'support': 'mohamedmtloob87@gmail.com',

    "summary": "User access restriction on warehouse and journals",
    "description": """
        user access restriction on journals and warehouse
    """,
    "depends": ['stock','account'],
    "data": [
        'security/stock_security.xml',
        'views/res_users_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
