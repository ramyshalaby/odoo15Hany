# -*- coding: utf-8 -*-
{
    'name': 'HR Allowances and Deduction',

    'summary': """
        Add Allowances and Deduction  General Rule .
    """,

    'description': """
		Allowances and Deduction screen  per Departments or tags or Employees
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
        'data/hr_role_seq.xml',
        'data/rule_date.xml',
        'security/hr_payroll_security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_role_view.xml'
    ],

}
