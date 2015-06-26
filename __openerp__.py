# -*- coding: utf-8 -*-
{
    'name': "Odoo_Academic",

    'summary': """
        Proceso""",

    'description': """
        Modulo de Open Academy para Entrenamiento
    """,

    'author': "Emiliano Quinodoz",
    'website': "http://www.emilianoquinodoz.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'views/session_view.xml',
        'views/session_workflow.xml',
        'views/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'views/demo.xml',
    ],
}
