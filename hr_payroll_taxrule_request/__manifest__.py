# -*- coding: utf-8 -*-
{
    'name': 'HR Income Tax Egypt Rule',
    'summary': """
        Calc Deduction for egypt tax as payslip rule .
    """,
    'description': """
		Egypt Income Tax as Deduction rule
                    """,
    'author': 'Mohamed Mtloob.',
    'license': 'OPL-1',

    'website': 'https://www.linkedin.com/in/mohamed-mtloob-62b33b76/',
    'license': 'OPL-1',
    'support': 'mohamedmtloob87@gmail.com',
    'maintainer': 'Mohamed Mtloob.',
    'category': 'HR',
    'version': '15.0.1.0.2',
    'depends': ['hr_payroll_community'],
    'data': [
        'security/ir.model.access.csv',
        'data/rule_date.xml',
        'views/income_tax_levels_view.xml',
    ],

}
