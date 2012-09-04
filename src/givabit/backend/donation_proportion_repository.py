from givabit.backend.donation_proportion import DonationProportion
from givabit.backend.payment import Payment
from givabit.backend.user import User

from google.appengine.ext import db

class DonationProportionRepository(object):
    @db.transactional
    def add_donation_proportion(self, donation_proportion):
        existing = self.get_donation_proportions(user=donation_proportion.user, charity=donation_proportion.charity)
        db.delete(existing)
        if donation_proportion.amount > 0:
            donation_proportion.put()

    def get_fraction(self, user, charity):
        """Gets the fraction of user's donation that should go to charity charity."""
        all_proportions = self.get_donation_proportions(user=user)
        numerator = 0
        denominator = 0
        for proportion in all_proportions:
            if proportion.charity == charity:
                # We may never have more than one donation proportion per charity per user
                numerator = proportion.amount
            denominator += proportion.amount
        if denominator == 0:
            return 0
        return float(numerator) / denominator

    def get_donation_proportions(self, user=None, charity=None):
        """Gets the donation proportions filtered by user and/or charity.

        If user is unspecified, returns for all users.
        If charity is unspecified, returns for all charities.

        It does not make sense to specify charity without user, and the magnitude of DonationProportion.amount is relative to the user's other donations.
        """
        query = DonationProportion.all()
        if user is not None:
            query.ancestor(user.key())
        if charity is not None:
            query.filter('charity =', charity)
        return [dp for dp in query.run()]
