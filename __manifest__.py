# -*- coding: utf-8 -*-
{
    'name': "pagoaprod",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
        'views/partner.xml',
        'views/reporte_conciliacion.xml',
        'views/reporte_factura.xml',
        'views/reporte_nomina.xml',
        'data/pagoaprod.cargo.csv',
    # En res.partner defino los datos de la entidad y socios    
        'data/res.partner.csv',
    # En pagoaprod.pagoaprod referencio los datos de la entidad anterior        
        'data/pagoaprod.pagoaprod.csv',
    # En pagoaprod.socio referencio la entidad y los socios creados anteriormente    
        'data/pagoaprod.socio.csv',
        'data/product.template.csv',
        'data/product.attribute.csv',
        'data/product.attribute.value.csv',
        'data/product.template.attribute.line.csv',
        'data/pagoaprod.mes.csv',
        'data/pagoaprod.anno.csv',
        'data/product.product.csv',
        'data/pagoaprod.insumo.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
