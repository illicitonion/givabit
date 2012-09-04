from givabit.backend.user import User

from google.appengine.ext import db

class DonationAmount(db.Model):
    user = db.ReferenceProperty(User)
    amount_GBPennies = db.IntegerProperty()

    @classmethod
    def new(cls, user, **kwargs):
        return DonationAmount(parent=user, user=user, **kwargs)

class DonationAmountRepository(object):
    def set_donation_amount(self, user, amount_GBPennies):
        user.donation_amount = amount_GBPennies
        user.put()

    def get_donation_amount(self, user):
        return user.donation_amount
