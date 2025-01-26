# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Geo Location Attendance',
    'version': '15.0.1.1',
    'summary': 'This module will only allows employee to check in/out within Active Work Location Range.| Geo Attendance | Remote Attendance | Human Resources | Employees | Geo Location | Active Work Location | Attendance Range | Active Location | CheckIn | CheckOut ',
    'description': """This module will get employees Geo Location and only allows them to check in/out within Active Work Location.
    """,
    'category': 'Human Resources/Attendances',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'images': ['static/description/banner.gif'],
    'depends': ['base_geolocalize', 'hr_attendance'],
    'data': [
        'views/attendance_location_view.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner.xml',
    ],
    'external_dependencies': {
        'python': ['geopy'],
    },
    'assets': {
        'web.assets_backend': [
            'geo_location_attendance_knk/static/src/js/my_attendances.js',
        ],
    },
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 50,
    'currency': 'EUR',
}
