from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'purchase.order'

    tracking_event_ids = fields.One2many(
        string='Tracking Events',
        comodel_name='tracking.event',
        inverse_name='purchase_id',
    )
    origin = fields.Char(copy=True)
