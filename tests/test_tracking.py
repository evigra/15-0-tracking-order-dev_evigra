from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase
from odoo.tests.common import Form


class TestTracking(TransactionCase):

    def setUp(self):
        super().setUp()
        self.sale_obj = self.env['sale.order']
        self.product = self.env['product.product'].create({'name': 'Test Product'})

    def create_partner(self):
        partner = Form(self.env['res.partner'])
        partner.name = 'Test Partner'
        return partner.save()

    def test_sale_tracking_auto(self):
        partner = self.create_partner()
        so_form = Form(self.sale_obj)
        so_form.partner_id = partner
        with so_form.order_line.new() as so_line:
            so_line.product_id = self.product
            so_line.product_uom_qty = 1.0
            so_line.price_unit = 10.0
        sale_order = so_form.save()
        self.assertRecordValues(sale_order.tracking_event_ids, [{
            'message': 'Sales Order created',
            'create_uid': self.env.uid,
            'source': 'internal',
        }])

    def test_02_tracking_state_constraint(self):
        """Testing the constraints of the model `tracking.event.state`:
        - Setting both fields beggining and closing state should raise an error saying that a state can't be
        the both types of state at the same time.
        - Setting the `beggining_state` field in True when there is a record with that field set in True, it should
        raise an error saying that there can't be 2 states set as a beggining one.
        - Setting the `closing_state` field in True when there is a record with that field set in True, it should
        raise an error saying that there can't be 2 states set as a closing one.
        """
        begginig_state = self.env.ref('tracking_order.tracking_state_not_shipped')
        closing_state = self.env.ref('tracking_order.tracking_state_delivered')
        state_model = self.env['tracking.event.state']

        both_states_error = "The state can't be a begginig state and a closing state at the same time."
        with self.assertRaises(ValidationError, msg=both_states_error):
            state_model.create({
                'name': "Test",
                'beggining_state': True,
                'closing_state': True,
            })

        begginig_state_error = "There's already one beggining state. Reference : %s" % begginig_state.name
        with self.assertRaises(ValidationError, msg=begginig_state_error):
            state_model.create({
                'name': "Test",
                'beggining_state': True,
            })

        closing_state_error = "There's already one closing state. Reference : %s" % closing_state.name
        with self.assertRaises(ValidationError, msg=closing_state_error):
            state_model.create({
                'name': "Test",
                'closing_state': True,
            })

    def test_03_sale_tracking_manual(self):
        """Testing the set of the message when changing the message type (it will be the description of the
        message type).
        """
        partner = self.create_partner()
        so_form = Form(self.sale_obj)
        so_form.partner_id = partner
        with so_form.order_line.new() as so_line:
            so_line.product_id = self.product
            so_line.product_uom_qty = 1.0
            so_line.price_unit = 10.0
        sale_order = so_form.save()
        self.assertRecordValues(sale_order.tracking_event_ids, [{
            'message': 'Sales Order created',
            'create_uid': self.env.uid,
            'source': 'internal',
        }])

        message_event = self.env['tracking.event.message'].create({
            'name': 'Testing Message',
            'description': 'Testing Message Description',
        })

        with Form(sale_order) as order:
            with order.tracking_event_ids.new() as event:
                event.message_type_id = message_event

        self.assertRecordValues(sale_order.tracking_event_ids, [
            {
                'message': 'Sales Order created',
                'create_uid': self.env.uid,
                'source': 'internal',
            },
            {
                'message': 'Testing Message Description',
                'create_uid': self.env.uid,
                'source': 'manual',
            },
        ])
