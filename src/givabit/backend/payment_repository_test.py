import test_data
import test_utils

from donation_proportion import DonationProportion
from donation_proportion_repository import DonationProportionRepository
from payment import OutgoingPayment, OutgoingPaymentState, Payment
from payment_repository import PaymentRepository

class PaymentRepositoryTest(test_utils.TestCase):

    def testAggregatesCharityTotalsAcrossUsers(self):
        self.add_confirmed_users([test_data.u1, test_data.u2])
        self.add_charities([test_data.c1, test_data.c2])

        payment_repo = PaymentRepository()
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
