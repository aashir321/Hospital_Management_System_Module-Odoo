{
    'name': 'Hospital Management System',
    'version': '1.0.0',
    'category': 'Healthcare',
    'sequence': -100,
    'application': True,
    'summary': 'A module for managing hospital operations',
    'description': 'This module provides features for managing patients, doctors, appointments, and medical records in a hospital setting.',
    'author': 'aashir',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/doctor_view.xml',
        'report/report.xml',
        'report/patient_report.xml',
        'report/report_style.xml',
        'views/patient_view.xml',
        'views/female_patients_view.xml',
        'views/appointment_view.xml',
    ]
}
