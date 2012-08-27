import test_data
import test_utils

from donation_proportion import DonationProportion
from payment import Payment

class DonationProportionRepositoryTest(test_utils.TestCase):

    def setUp(self):
        super(DonationProportionRepositoryTest, self).setUp()
        self.add_confirmed_users([test_data.u1, test_data.u2])
        self.add_charities([test_data.c1, test_data.c2, test_data.c3])

    def test_can_add_donation_proportions(self):
        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=2),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=6),
        ])

        self.assertEquals(0.25, self.dp_repo.get_fraction(user=test_data.u1, charity=test_data.c1))
        self.assertEquals(0.75, self.dp_repo.get_fraction(user=test_data.u1, charity=test_data.c2))
        self.assertEquals(0, self.dp_repo.get_fraction(user=test_data.u1, charity=test_data.c3))

    def test_no_donations_gives_fractions_as_zero(self):
        self.assertEquals(0, self.dp_repo.get_fraction(user=test_data.u1, charity=test_data.c1))

    def test_updates_multiple_donations(self):
        dp = DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=1)
        self.dp_repo.add_donation_proportion(dp)
        self.assertSequenceEqual(self.dp_repo.get_donation_proportions(user=test_data.u1), [dp])

        dp2 = DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=2)
        self.dp_repo.add_donation_proportion(dp2)
        self.assertSequenceEqual(self.dp_repo.get_donation_proportions(user=test_data.u1), [dp2])

    def test_donation_proportions_are_isolated_per_user(self):
        self.add_donation_proportions([
            DonationProportion.new(user=test_data.u1, charity=test_data.c1, amount=1),
            DonationProportion.new(user=test_data.u1, charity=test_data.c2, amount=1),
            DonationProportion.new(user=test_data.u2, charity=test_data.c1, amount=1),
        ])
        self.assertEquals(0.5, self.dp_repo.get_fraction(user=test_data.u1, charity=test_data.c1))
