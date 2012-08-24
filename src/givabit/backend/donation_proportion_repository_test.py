import test_data
import test_utils

from donation_proportion import DonationProportion
from donation_proportion_repository import DonationProportionRepository

class DonationProportionRepositoryTest(test_utils.TestCase):

    def testCanAddDonationProportions(self):
        self.add_confirmed_users([test_data.u1])
        self.add_charities([test_data.c1, test_data.c2, test_data.c3])

        dp_repo = DonationProportionRepository()
        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=2),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=6),
        ], dp_repo)

        self.assertEquals(0.25, dp_repo.get_fraction(user=test_data.u1, charity=test_data.c1))
        self.assertEquals(0.75, dp_repo.get_fraction(user=test_data.u1, charity=test_data.c2))
        self.assertEquals(0, dp_repo.get_fraction(user=test_data.u1, charity=test_data.c3))

    def testNoDonationsGivesFractionsAsZero(self):
        self.add_confirmed_users([test_data.u1])
        self.add_charities([test_data.c1])

        self.assertEquals(0, DonationProportionRepository().get_fraction(user=test_data.u1, charity=test_data.c1))

    def testUpdatesMultipleDonations(self):
        self.add_confirmed_users([test_data.u1])
        self.add_charities([test_data.c1])

        dp_repo = DonationProportionRepository()
        dp = DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=1)
        dp_repo.add_donation_proportion(dp)
        self.assertSequenceEqual(dp_repo.get_donation_proportions(user=test_data.u1), [dp])

        dp2 = DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=2)
        dp_repo.add_donation_proportion(dp2)
        self.assertSequenceEqual(dp_repo.get_donation_proportions(user=test_data.u1), [dp2])

    def testDonationProportionsAreIsolatedPerUser(self):
        self.add_confirmed_users([test_data.u1, test_data.u2])
        self.add_charities([test_data.c1, test_data.c2])

        dp_repo = DonationProportionRepository()
        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=1),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=1),
            DonationProportion.new(user=test_data.u2, charity=test_data.c1, amount=1),
        ], dp_repo)
        self.assertEquals(0.5, dp_repo.get_fraction(user=test_data.u1, charity=test_data.c1))
