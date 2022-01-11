from odoo import api, fields, models
from lxml import html


class TrackingEvent(models.Model):
    _name = 'tracking.event'
    _description = 'Tracking Event'
    _order = 'date_created asc'
    _inherit = 'mail.thread'

    picking_id = fields.Many2one(
        string='Stock Picking',
        comodel_name='stock.picking',
    )
    sale_id = fields.Many2one(
        string='Sale Order',
        comodel_name='sale.order',
    )
    purchase_id = fields.Many2one(
        string='Purchase Order',
        comodel_name='purchase.order',
    )
    source = fields.Selection(
        [
            ('manual', 'Manual'),
            ('internal', 'Odoo Internal')
        ],
        required=True,
        readonly=True,
        default='manual',
        help="Origin from where the action was performed",
    )
    date_created = fields.Datetime(
        default=lambda s: fields.Datetime.now(),
    )
    create_uid = fields.Many2one(
        'res.users',
        readonly=True,
        default=lambda self: self.env.uid,
        string="Created By"
    )
    message_type_id = fields.Many2one(
        'tracking.event.message',
    )
    message = fields.Char(
        required=True,
        help="Description of the tracking event",
    )
    reference = fields.Char(
        help='Identifies the records to whom the tracking is registered',
    )
    location_id = fields.Many2one('tracking.event.location')
    state_id = fields.Many2one('tracking.event.state')

    @api.model
    def _get_selection_state(self):
        field = self.fields_get(allfields=['source'])
        return field['source']['selection']

    def name_get(self):
        res = []
        for rec_id in self:
            try:
                source = rec_id.state.capitalize()
            except AttributeError:
                source = 'UNKNOWN'
            name = '[{source}]'.format(source=source)
            res.append((rec_id.id, name))
        return res

    def create_event(self, model, record_id, message, source):
        tracking_models = {'sale.order': 'sale_id', 'purchase.order': 'purchase_id', 'stock.picking': 'picking_id'}
        reated_field = tracking_models[model]
        message_post = str(html.fromstring(message).text_content()) if message != '' else message
        model_title = ' '.join(model.split('.')).title()
        record = self.env[model].browse(record_id)
        reference = '%s: %s' % (model_title, record.name)
        vals = {
            reated_field: record_id,
            'message': message_post,
            'source': source,
            'reference': reference,
        }
        if source == 'manual':
            return self.create(vals)

        beggining_state = self.env['tracking.event.state'].search([('beggining_state', '=', True)], limit=1)
        state_id = beggining_state.id
        location_id = False
        if model == 'stock.picking':
            location_id = record.location_dest_id.event_tracking_location_id.id
            if record.state == 'done':
                closing_state = self.env['tracking.event.state'].search([('closing_state', '=', True)], limit=1)
                state_id = closing_state.id
        vals.update({
            'location_id': location_id,
            'state_id': state_id,
        })
        self.create(vals)

    @api.onchange('message_type_id')
    def _onchange_message_type_id(self):
        self.message = self.message_type_id.description
