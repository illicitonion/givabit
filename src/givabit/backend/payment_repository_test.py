import test_data
import test_utils

from amount_mismatch import AccumulatingMismatchNotifier, AmountMismatch
from donation_proportion import DonationProportion
from payment import IncomingPayment, OutgoingPayment, OutgoingPaymentState, Payment

class PaymentRepositoryTest(test_utils.TestCase):

    def setUp(self):
        super(PaymentRepositoryTest, self).setUp()
        self.add_confirmed_users([test_data.u1, test_data.u2, test_data.u3, test_data.u4, test_data.u5])
        self.add_charities([test_data.c1, test_data.c2])


    def test_aggregates_charity_totals_across_users(self):
        self.setup_one_incoming_payment({
            test_data.u1: 250,
            test_data.u2: 75
        })

        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=100),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=150),
            DonationProportion.new(user=test_data.u2, charity=test_data.c1, amount=75),
        ])

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=175, status=OutgoingPaymentState.DISPLAYED),
            OutgoingPayment(charity=test_data.c2, amount_GBPennies=150, status=OutgoingPaymentState.DISPLAYED),
        ])

        self.assertEquals(self.payment_repo.get_pending_outgoing_payments(), expected)

    def test_only_generates_outgoing_payments_if_incoming_payments_received(self):
        self.setup_one_incoming_payment({test_data.u1: 250})
        self.setup_one_missing_payment({test_data.u2: 75})

        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=100),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=150),
            DonationProportion.new(user=test_data.u2, charity=test_data.c1, amount=75),
        ])

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=100, status=OutgoingPaymentState.DISPLAYED),
            OutgoingPayment(charity=test_data.c2, amount_GBPennies=150, status=OutgoingPaymentState.DISPLAYED),
        ])

        self.assertEquals(self.payment_repo.get_pending_outgoing_payments(), expected)

    def test_logs_and_notifies_incoming_and_outgoing_mismatches(self):
        self.setup_one_mismatched_incoming_payment({
            test_data.u1: (250, 249),
            test_data.u2: (250, 251),
            test_data.u4: (200, 200),
            test_data.u5: (75, 75),
        })
        self.setup_one_missing_payment({test_data.u3: 10})

        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=100),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=150),
            DonationProportion.new(user=test_data.u2, charity=test_data.c1, amount=250),
            DonationProportion.new(user=test_data.u3, charity=test_data.c1, amount=10),
            DonationProportion.new(user=test_data.u5, charity=test_data.c1, amount=75),
        ])

        amount_mismatch_notifier = AccumulatingMismatchNotifier()
        self.payment_repo.get_pending_outgoing_payments(amount_mismatch_notifiers=[amount_mismatch_notifier])

        expected = set([
            AmountMismatch(user=test_data.u1, incoming_GBPennies=249, outgoing=[
                OutgoingPayment(charity=test_data.c1, amount_GBPennies=100, status=OutgoingPaymentState.VALUE_MISMATCH),
                OutgoingPayment(charity=test_data.c2, amount_GBPennies=150, status=OutgoingPaymentState.VALUE_MISMATCH),
            ]),
            AmountMismatch(user=test_data.u2, incoming_GBPennies=251, outgoing=[OutgoingPayment(charity=test_data.c1, amount_GBPennies=250, status=OutgoingPaymentState.VALUE_MISMATCH)]),
            AmountMismatch(user=test_data.u3, incoming_GBPennies=0, outgoing=[OutgoingPayment(charity=test_data.c1, amount_GBPennies=10, status=OutgoingPaymentState.VALUE_MISMATCH)]),
            AmountMismatch(user=test_data.u4, incoming_GBPennies=200, outgoing=[]),
        ])

        self.assertEquals(amount_mismatch_notifier.accumulated, expected)

    def test_generates_outgoing_payments_despite_mismatches(self):
        self.setup_one_incoming_payment({
            test_data.u1: 100,
            test_data.u2: 75,
        })

        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=100),
        ])

        expected = set([
            OutgoingPayment(charity=test_data.c1, amount_GBPennies=100, status=OutgoingPaymentState.DISPLAYED),
        ])
        expected_notifications = set([
            AmountMismatch(user=test_data.u2, incoming_GBPennies=75, outgoing=[]),
        ])

        amount_mismatch_notifier = AccumulatingMismatchNotifier()
        self.assertEquals(self.payment_repo.get_pending_outgoing_payments(amount_mismatch_notifiers=[amount_mismatch_notifier]), expected)
        self.assertEquals(amount_mismatch_notifier.accumulated, expected_notifications)

    def test_adding_donation_proportion_adds_payments_if_amount_set_first(self):
        self.da_repo.set_donation_amount(user=test_data.u1, amount_GBPennies=100)

        self.dp_repo.add_donation_proportion(DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=2))
        expected = [Payment(user=test_data.u1, charity=test_data.c1, amount_GBPennies=100)]

        self.assertEquals(self.payment_repo.get_next_expected_payments(user=test_data.u1), expected)

        self.dp_repo.add_donation_proportion(DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=3))
        expected = [
            Payment(user=test_data.u1, charity=test_data.c1, amount_GBPennies=40),
            Payment(user=test_data.u1, charity=test_data.c2, amount_GBPennies=60),
        ]

        self.assertEquals(self.payment_repo.get_next_expected_payments(user=test_data.u1), expected)
