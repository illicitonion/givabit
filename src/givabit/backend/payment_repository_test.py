import test_data
import test_utils

from donation_proportion import DonationProportion
from donation_proportion_repository import DonationProportionRepository
from payment import IncomingPayment, OutgoingPayment, OutgoingPaymentState, Payment
from payment_repository import PaymentRepository

class PaymentRepositoryTest(test_utils.TestCase):

    def setUp(self):
        super(PaymentRepositoryTest, self).setUp()
        self.add_confirmed_users([test_data.u1, test_data.u2])
        self.add_charities([test_data.c1, test_data.c2])


    def test_aggregates_charity_totals_across_users(self):
        payment_repo = PaymentRepository()

        self.add_incoming_payments([
            IncomingPayment(user=test_data.u1, amount_GBPennies=250),
            IncomingPayment(user=test_data.u2, amount_GBPennies=75),
        ], payment_repo)

        self.add_payments([
            Payment.new(user=test_data.u1, charity=test_data.c1, amount_GBPennies=100),
            Payment.new(user=test_data.u1, charity=test_data.c2, amount_GBPennies=150),
            Payment.new(user=test_data.u2, charity=test_data.c1, amount_GBPennies=75),
        ], payment_repo)

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=175, state=OutgoingPaymentState.DISPLAYED),
            OutgoingPayment(charity=test_data.c2, amount_GBPennies=150, state=OutgoingPaymentState.DISPLAYED),
        ])

        self.assertEquals(payment_repo.get_pending_outgoing_payments(), expected)

    def test_only_generates_outgoing_payments_if_incoming_payments_received(self):
        payment_repo = PaymentRepository()

        self.add_incoming_payments([
            IncomingPayment(user=test_data.u1, amount_GBPennies=250),
        ], payment_repo)

        self.add_payments([
            Payment.new(user=test_data.u1, charity=test_data.c1, amount_GBPennies=100),
            Payment.new(user=test_data.u1, charity=test_data.c2, amount_GBPennies=150),
            Payment.new(user=test_data.u2, charity=test_data.c1, amount_GBPennies=75),
        ], payment_repo)

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=100, state=OutgoingPaymentState.DISPLAYED),
            OutgoingPayment(charity=test_data.c2, amount_GBPennies=150, state=OutgoingPaymentState.DISPLAYED),
        ])

        self.assertEquals(payment_repo.get_pending_outgoing_payments(), expected)
