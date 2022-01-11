from odoo import api, models


class MailMesssage(models.Model):
    _inherit = "mail.message"

    @api.model_create_multi
    def create(self, values_list):
        res = super().create(values_list)
        tracking_event = self.env['tracking.event']
        model_tracking = ['sale.order', 'purchase.order', 'stock.picking']
        for record in res:
            message = self._get_message(record)
            if record.model in model_tracking and message != '':
                tracking_event.create_event(record.model, record.res_id, message, 'internal')
        return res

    def _get_message(self, message):
        note = self.env.ref('mail.mt_note')

        if message.subtype_id and message.subtype_id != note:
            return (' - ').join([message.subtype_id.name, message.message_type])
        if message.body.find('created') != -1:
            return message.body
        if message.tracking_value_ids:
            return message.tracking_value_ids[0].new_value_char or ''
        return ''
