import unittest
import uuid

from givabit.backend.charity_repository import CharityRepository
from givabit.backend.donation_amount_repository import DonationAmountRepository
from givabit.backend.donation_proportion_repository import DonationProportionRepository
from givabit.backend.payment import IncomingPayment
from givabit.backend.payment_repository import PaymentRepository
from givabit.backend.session_repository import SessionRepository
from givabit.backend.user import User
from givabit.backend.user_repository import UserRepository

from givabit.test_common import test_data

from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed

class TestUser(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

class TestCase(unittest.TestCase):
    def setUp(self):
        reload(test_data)
        self.set_up_database()

        self.charity_repo = CharityRepository()
        self.da_repo = DonationAmountRepository()
        self.dp_repo = DonationProportionRepository()
        self.payment_repo = PaymentRepository(self.dp_repo)
        self.user_repo = UserRepository()
        self.session_repo = SessionRepository(self.user_repo)

    def tearDown(self):
        self.tear_down_database()

    def set_up_database(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=policy)
        self.testbed.init_mail_stub()

    def tear_down_database(self):
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

    def create_ready_to_use_user(self):
        email = '%s@%s.com' % (uuid.uuid4(), TestCase.get_and_increment_random_index())
        password = str(uuid.uuid4())
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        self.user_repo.confirm_user(email=new_user.email, confirmation_code=new_user.confirmation_code)
        self.user_repo.set_password(email=new_user.email, password=password, confirmation_code=new_user.confirmation_code)
        return TestUser(email, password)

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

    def get_only_sent_email(self, to):
        mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        messages = mail_stub.get_sent_messages(to=to)
        self.assertEquals(len(messages), 1)
        return messages[0]

    @classmethod
    def get_and_increment_random_index(cls):
        if not hasattr(cls, 'random_index'):
            cls.random_index = -1
        cls.random_index += 1
        return cls.random_index

    def get_random_value(self):
        return str(uuid.uuid4())
