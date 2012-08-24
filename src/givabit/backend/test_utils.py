import test_data
import unittest

from charity_repository import CharityRepository
from donation_proportion_repository import DonationProportionRepository
from google.appengine.ext import testbed
from user_repository import UserRepository

class TestCase(unittest.TestCase):
    def setUp(self):
        reload(test_data)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

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

