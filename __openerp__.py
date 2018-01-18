# -*- coding: utf-8 -*-
{
    'name': "Custom views for LCB reporting",
    'author': "QArea, Yury Stasovsky",
    'license': 'LGPL-3',
    'website' : "https://qarea.us",
    'category': 'Custom integration',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sce', 'sale_order_lot_selection'],
#    'depends': ['sale', 'purchase', 'mrp', 'sce'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'security/groups.xml',
       # 'wizard/wiz_view.xml',
        'views/stock_inventory_line.xml',
        'views/sale_order_line.xml',
        'views/pos_order_line.xml',
        'views/stock_picking.xml',
        'views/product_product.xml',
        #'views/menu.xml',
    ],
    'installable': True,
}
