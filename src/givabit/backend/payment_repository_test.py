import test_data
import test_utils

from amount_mismatch import AccumulatingMismatchNotifier, AmountMismatch
from donation_proportion import DonationProportion
from donation_proportion_repository import DonationProportionRepository
from payment import IncomingPayment, OutgoingPayment, OutgoingPaymentState, Payment
from payment_repository import PaymentRepository

class PaymentRepositoryTest(test_utils.TestCase):

    def setUp(self):
        super(PaymentRepositoryTest, self).setUp()
        self.add_confirmed_users([test_data.u1, test_data.u2, test_data.u3, test_data.u4, test_data.u5])
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

    def test_logs_and_notifies_incoming_and_outgoing_mismatches(self):
        payment_repo = PaymentRepository()

        self.add_incoming_payments([
            IncomingPayment(user=test_data.u1, amount_GBPennies=249),
            IncomingPayment(user=test_data.u2, amount_GBPennies=251),
            IncomingPayment(user=test_data.u4, amount_GBPennies=200),
            IncomingPayment(user=test_data.u5, amount_GBPennies=75),
        ], payment_repo)

        self.add_payments([
            Payment.new(user=test_data.u1, charity=test_data.c1, amount_GBPennies=100),
            Payment.new(user=test_data.u1, charity=test_data.c2, amount_GBPennies=150),
            Payment.new(user=test_data.u2, charity=test_data.c1, amount_GBPennies=250),
            Payment.new(user=test_data.u3, charity=test_data.c1, amount_GBPennies=10),
            Payment.new(user=test_data.u5, charity=test_data.c1, amount_GBPennies=75),
        ], payment_repo)

        amount_mismatch_notifier = AccumulatingMismatchNotifier()
        payment_repo.get_pending_outgoing_payments([amount_mismatch_notifier])

        expected = set([
            AmountMismatch(user=test_data.u1, incoming_GBPennies=249, outgoing=[
                OutgoingPayment.new(charity=test_data.c1, amount_GBPennies=100, status=OutgoingPaymentState.VALUE_MISMATCH),
                OutgoingPayment.new(charity=test_data.c2, amount_GBPennies=150, status=OutgoingPaymentState.VALUE_MISMATCH),
            ]),
            AmountMismatch(user=test_data.u2, incoming_GBPennies=251, outgoing=[OutgoingPayment.new(charity=test_data.c1, amount_GBPennies=250, status=OutgoingPaymentState.VALUE_MISMATCH)]),
            AmountMismatch(user=test_data.u3, incoming_GBPennies=0, outgoing=[OutgoingPayment.new(charity=test_data.c1, amount_GBPennies=10, status=OutgoingPaymentState.VALUE_MISMATCH)]),
            AmountMismatch(user=test_data.u4, incoming_GBPennies=200, outgoing=[]),
        ])

        self.assertEquals(amount_mismatch_notifier.accumulated, expected)

    def test_generates_outgoing_payments_despite_mismatches(self):
        payment_repo = PaymentRepository()

        self.add_incoming_payments([
            IncomingPayment(user=test_data.u1, amount_GBPennies=100),
            IncomingPayment(user=test_data.u2, amount_GBPennies=75),
        ], payment_repo)

        self.add_payments([
            Payment.new(user=test_data.u1, charity=test_data.c1, amount_GBPennies=100),
        ], payment_repo)

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=100, state=OutgoingPaymentState.DISPLAYED),
        ])
        expected_notifications = set([
            AmountMismatch(user=test_data.u2, incoming_GBPennies=75, outgoing=[]),
        ])

        amount_mismatch_notifier = AccumulatingMismatchNotifier()
        self.assertEquals(payment_repo.get_pending_outgoing_payments([amount_mismatch_notifier]), expected)
        self.assertEquals(amount_mismatch_notifier.accumulated, expected_notifications)
