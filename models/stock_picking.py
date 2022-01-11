from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tracking_event_ids = fields.One2many(
        string='Tracking Events',
        comodel_name='tracking.event',
        inverse_name='picking_id',
    )
