# -*- coding: utf-8 -*-
###################################################################################
#    A part of Mtloob Project <https://www.Mtloob.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2021-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Ijaz Ahammed (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Diar Overtime/Parttime Request',
    'version': '15.0.1.0.1',
    'summary': 'Manage Employee Overtime/Parttime',
    'description': """
        Helps you to manage Employee Overtime/Parttime.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': 'Mohamed Mtloob',
    'company': 'Mtloob Solutions',
    'maintainer': 'Mohamed Mtloob Solutions',
    'website': 'https://www.linkedin.com/in/mohamed-mtloob-62b33b76/',
    'depends': [
        'hr', 'hr_contract', 'hr_attendance', 'hr_holidays', 'project', 'hr_payroll_community'
    ],
    'external_dependencies': {
        'python': ['pandas'],
    },
    'data': [
        'security/overtime_security.xml',
        'security/parttime_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/hr_overtime_demo.xml',
        'views/overtime_request_view.xml',
        'views/overtime_type.xml',
        'views/hr_contract.xml',
        'views/hr_payslip.xml',
        'views/hr_job_view.xml',
        'views/hr_employee_view.xml',
        'views/social_insurance_view.xml',
    ],
    'demo': ['data/hr_overtime_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
