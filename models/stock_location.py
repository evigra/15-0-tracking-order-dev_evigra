# Copyright 2021 Vauxoo

from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    event_tracking_location_id = fields.Many2one(
        'tracking.event.location',
        domain="[('location_type', '=', 'internal')]")
