# -*- coding: utf-8 -*-
{
    'name': "Diar Project Dashboard",

    'summary': """
        User and Manager can add project data for final dashboard.""",

    'description': """
        With the help of this module you can manage manager can review and project data and dashboard.
    """,

    'author': "Mohamed Mtloob.",
    'website': "https://www.linkedin.com/in/mohamed-mtloob-62b33b76/",
    'category': "tools",
    'version': "15.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet', 'project','report_xlsx', 'board'],

    # always loaded
    'data': [
        'security/doc_submital_log_security.xml',
        'security/ir.model.access.csv',
        'data/docsublog_seq.xml',
        'views/project_dashboard_view.xml',
        'views/doc_submital_log_view.xml',
        'views/doc_submital_sd_log_view.xml',
        'views/discipline_section_view.xml',
        'views/contract_type_view.xml',
        'views/inspection_request_log_view.xml',
        'views/material_inspection_request_log_view.xml',
        'views/material_submittal_log_view.xml',
        'views/request_for_information_log_view.xml',
        'views/non_conformance_report_log_view.xml',
    ],
    'images': [],
    'autoinstall': False,
    'installable': True,
    'application': False
}
