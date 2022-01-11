# Copyright 2021 Vauxoo

from odoo import fields, models


class TrackingEventLocation(models.Model):
    _name = 'tracking.event.location'
    _description = 'Tracking Event Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        required=True,
        tracking=True,
    )
    location_type = fields.Selection(
        [('internal', 'Internal'),
         ('external', 'External'),
         ], required=True,
        tracking=True,
    )
