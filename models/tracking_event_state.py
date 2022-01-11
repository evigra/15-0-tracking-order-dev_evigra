# Copyright 2021 Vauxoo

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TrackingEventState(models.Model):
    _name = 'tracking.event.state'
    _description = 'Tracking Event State'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        tracking=True,
        translate=True,
    )
    sequence = fields.Integer(default=5)
    beggining_state = fields.Boolean(tracking=True)
    closing_state = fields.Boolean(tracking=True)

    @api.constrains('beggining_state', 'closing_state')
    def _check_stage(self):
        both_states_error = _("The state can't be a begginig state and a closing state at the same time.")
        begginig_state_error = _("There's already one beggining state. Reference : %s")
        closing_state_error = _("There's already one closing state. Reference : %s")
        for state in self.filtered(lambda state: state.beggining_state or state.closing_state):
            if state.beggining_state and state.closing_state:
                raise ValidationError(both_states_error)

            begginig_state = self.search([('id', '!=', state.id), ('beggining_state', '=', True)], limit=1)
            if state.beggining_state and begginig_state:
                raise ValidationError(begginig_state_error % begginig_state.name)

            closing_state = state.search([('id', '!=', state.id), ('closing_state', '=', True)], limit=1)
            if state.closing_state and closing_state:
                raise ValidationError(closing_state_error % closing_state.name)
