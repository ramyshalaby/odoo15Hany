# -*- coding: utf-8 -*-
{
    'name': "Diar Timesheet Approval",

    'summary': """
        Manager can approve and reject the time sheet of an employee.""",

    'description': """
        With the help of this module you can manage manager can approve or reject the time sheet and it automatically send the mail to 
        the employee.
    """,

    'author': "Mohamed Mtloob.",
    'website': "https://www.linkedin.com/in/mohamed-mtloob-62b33b76/",
    'category': "tools",
    'version': "15.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet','hr_attendance_sheet','project'],

    # always loaded
    'data': [
        'security/timesheet_approval_security.xml',
        'data/email_template.xml',
        'data/timesheet_approval_serveraction.xml',
        'report/attendance_sheet_report.xml',
        'views/timesheet_validation_view.xml',
        'views/project_project_view.xml',
    ],

    
    'images': [],
    'autoinstall': False,
    'installable': True,
    'application': False
}
