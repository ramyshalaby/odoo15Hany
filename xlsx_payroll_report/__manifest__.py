# -*- coding: utf-8 -*-
{
    "name": "Excel Payroll Report",
    "summary": "A payroll report in xlsx format",
    "version": "16.0",
    'author': 'Mohamed Mtloob.',
    'website': 'https://www.linkedin.com/in/mohamed-mtloob-62b33b76/',
    'license': 'OPL-1',
    'support': 'mohamedmtloob87@gmail.com',

    'maintainer': 'Mohamed Mtloob.',
    "category": "Human Resources/Payroll",
    "depends": ['hr_payroll_community','report_xlsx'],
    "data": [
        'security/ir.model.access.csv',
        'wizard/hr_payslip_xlsx_report_view.xml',
        'views/hr_payslip_view.xml',
        # 'data/server_action.xml',
        'report/payroll_report.xml',

    ],
    "images": [
        'images/main_screenshot.png'
    ],
    "installable": True,
}
