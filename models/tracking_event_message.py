# Copyright 2021 Vauxoo

from odoo import fields, models


class TrackingEventMessage(models.Model):
    _name = 'tracking.event.message'
    _description = 'Tracking Event Message'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        required=True,
        tracking=True,
        translate=True,
    )
    description = fields.Char(
        required=True,
        tracking=True,
    )
