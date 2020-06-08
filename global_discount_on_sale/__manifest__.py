# -*- coding: utf-8 -*-
{
    'name': "Global Discount on Sale Order",
    'summary': """
        Customisation to provide global discount on Sale Order.
        """,
    'description': """
    Customisation to provide global discount on Sale Order. The global
    discount will be affected on invoice and related journal.
        """,
    'version': '12.0.1.0.0',
    'author': "Aktiv Software",
    'website': "www.aktivsoftware.com",
    "category": "Sales",
    'depends': ['sale_management'],
    'data': [
        'security/security.xml',
        'views/account_invoice_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_views.xml',
        'report/sale_report_templates.xml',
        'report/report_invoice.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
