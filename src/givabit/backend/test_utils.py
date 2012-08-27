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

    def tearDown(self):
        self.testbed.deactivate()

    def add_charities(self, charities, charity_repository=None):
        if charity_repository is None:
            charity_repository = CharityRepository()
        for charity in charities:
            charity_repository.add_or_update_charity(charity)

    def add_donation_proportions(self, dps, dp_repo=None):
        if dp_repo is None:
            dp_repo = DonationProportionRepository()
        for dp in dps:
            dp_repo.add_donation_proportion(dp)

    def add_confirmed_users(self, users, user_repository=None):
        if user_repository is None:
            user_repository = UserRepository()
        for user in users:
            user_repository.create_confirmed_user_FOR_TEST(user)

    def add_payments(self, payments, payment_repository=None):
        if payment_repository is None:
            payment_repository = PaymentRepository()
        for payment in payments:
            payment_repository.add_payment(payment)

    def add_incoming_payments(self, incoming_payments, payment_repository=None):
        if payment_repository is None:
            payment_repository = PaymentRepository()
        for incoming_payment in incoming_payments:
            payment_repository.add_incoming_payment(incoming_payment)

    def setup_one_incoming_payment(self, users_and_amounts, payment_repo, da_repo):
        # users_and_amounts: {user: amount}
        for (user, amount) in users_and_amounts.items():
            self.setup_one_mismatched_incoming_payment({user: (amount, amount)}, payment_repo, da_repo)

    def setup_one_mismatched_incoming_payment(self, users_to_payments, payment_repo, da_repo):
        # users_to_payments : {user: (expected, actual)}
        for (user, (expected, actual)) in users_to_payments.items():
            da_repo.set_donation_amount(user=user, amount_GBPennies=expected)
            payment_repo.add_incoming_payment(IncomingPayment(user=user, amount_GBPennies=actual))

    def setup_one_missing_payment(self, users_to_payments, da_repo):
        # users_and_amounts: {user: amount}
        for (user, amount) in users_to_payments.items():
            da_repo.set_donation_amount(user=user, amount_GBPennies=amount)
