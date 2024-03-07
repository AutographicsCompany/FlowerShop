{
    'name': 'Flower Shop',
    'summary': 'Flowers Shop',
    'description': """
    This is a custom module for a flower shop.
    """,
    'depends': [
        'sale_management', 'product', 'website',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/actions.xml',
        'data/paper_format.xml',
        'views/main_flower_view.xml',
        'views/iflower_product.xml',
        'views/website_flower_shop.xml',
        'views/stock_production_lot.xml',
        'views/sale_order.xml',
        # Ensure that stock_warehouse_weather.xml is loaded after stock.view_warehouse definition
        'views/stock_warehouse_weather.xml',
        # Add the new XML file for scheduled actions
        'views/stock_warehouse_scheduled_actions.xml',
        'views/menu.xml',
        'reports/sale_order_flowers.xml',
    ],

    'installable': True,
    'auto_install': True,  # Set to True if you want it to be auto-installed
    'application': True,
    'license': 'LGPL-3',
    'sequence': 3,
}
