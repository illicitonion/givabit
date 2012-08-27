import test_data
import unittest

from charity_repository import CharityRepository
from donation_amount_repository import DonationAmountRepository
from donation_proportion_repository import DonationProportionRepository
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed
from payment import IncomingPayment
from payment_repository import PaymentRepository
from user_repository import UserRepository

class TestCase(unittest.TestCase):
    def setUp(self):
        reload(test_data)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=policy)

        self.charity_repo = CharityRepository()
        self.da_repo = DonationAmountRepository()
        self.dp_repo = DonationProportionRepository()
        self.payment_repo = PaymentRepository()
        self.user_repo = UserRepository()

    def tearDown(self):
        self.testbed.deactivate()

    def add_charities(self, charities):
        for charity in charities:
            self.charity_repo.add_or_update_charity(charity)

    def add_donation_proportions(self, dps):
        for dp in dps:
            self.dp_repo.add_donation_proportion(dp)

    def add_confirmed_users(self, users):
        for user in users:
            self.user_repo.create_confirmed_user_FOR_TEST(user)

    def add_payments(self, payments, payment_repository=None):
        for payment in payments:
            self.payment_repo.add_payment(payment)

    def add_incoming_payments(self, incoming_payments):
        for incoming_payment in incoming_payments:
            self.payment_repo.add_incoming_payment(incoming_payment)

    def setup_one_incoming_payment(self, users_and_amounts):
        # users_and_amounts: {user: amount}
        for (user, amount) in users_and_amounts.items():
            self.setup_one_mismatched_incoming_payment({user: (amount, amount)})

    def setup_one_mismatched_incoming_payment(self, users_to_payments):
        # users_to_payments : {user: (expected, actual)}
        for (user, (expected, actual)) in users_to_payments.items():
            self.da_repo.set_donation_amount(user=user, amount_GBPennies=expected)
            self.payment_repo.add_incoming_payment(IncomingPayment(user=user, amount_GBPennies=actual))

    def setup_one_missing_payment(self, users_to_payments):
        # users_and_amounts: {user: amount}
        for (user, amount) in users_to_payments.items():
            self.da_repo.set_donation_amount(user=user, amount_GBPennies=amount)
