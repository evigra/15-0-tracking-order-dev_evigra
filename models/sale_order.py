from odoo import api, models, fields, _


class StockPicking(models.Model):
    _inherit = 'sale.order'

    tracking_event_ids = fields.One2many(
        string='Tracking Events',
        comodel_name='tracking.event',
        inverse_name='sale_id',
    )

    tracking_event_count = fields.Integer(
        compute='_compute_events_count', readonly=True, help='Counts the tracking events related to this sale order')

    def _get_purchase_orders(self):
        purchase_order_ids = super()._get_purchase_orders()
        purchase_order_ids |= purchase_order_ids.search([('origin', '=ilike', self.name)])
        return purchase_order_ids

    @api.depends('order_line.purchase_line_ids.order_id', 'picking_ids')
    def _compute_events_count(self):
        for order in self:
            events = order._get_tracked_events()
            order.tracking_event_count = len(events)

    def _get_tracked_events(self):
        self.ensure_one()
        purchase_ids = self._get_purchase_orders()
        picking_ids = self.picking_ids | purchase_ids.mapped('picking_ids')
        domain = ['|', ('picking_id', 'in', picking_ids.ids), ('purchase_id', 'in', purchase_ids.ids)]
        events = self.env['tracking.event'].search(domain)
        events |= self.tracking_event_ids
        return events

    def action_views_tracking_event(self):
        self.ensure_one()
        events = self._get_tracked_events()
        action = {
            'res_model': 'tracking.event',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'name': _("Tracking events related to %s", self.name),
            'domain': [('id', 'in', events.ids)],
        }
        return action
