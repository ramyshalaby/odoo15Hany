# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name': 'Payslip Excel Report',
    'version': '15',
    'author': "Livedigital Technologies Private Limited",
    'website': "ldtech.in",
    'category': 'Payroll',
    'license': 'LGPL-3',
    'summary': 'Excel sheet for Payslip report',
    'description': """ Payslip excel report""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/payslip_xls_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
