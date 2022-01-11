{
    'name': 'Tracking Orders',
    'summary': '''
    Tracking from Sale Order and Purchase to Picking.
    ''',
    'author': 'Vauxoo',
    'website': 'http://www.vauxoo.com',
    'license': 'AGPL-3',
    'category': 'Installer',
    'version': '14.0.1.0.1',
    'depends': [
        # Official Modules
        'sale_management',
        'purchase',
        'stock',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/tracking_event_location_data.xml',
        'data/tracking_event_state_data.xml',

        'views/stock_picking_views.xml',
        'views/stock_location_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_views.xml',
        'views/tracking_event_views.xml',
        'views/tracking_event_location_views.xml',
        'views/tracking_event_message_views.xml',
        'views/tracking_event_state_views.xml',
    ],
    'demo': [
        'demo/tracking_event_message_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
