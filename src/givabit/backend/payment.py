from givabit.backend.charity import Charity
from givabit.backend.user import User

from google.appengine.ext import db

class Payment(object):
    """Represents a payment from a user to a charity.

    This payment is a translation of a DonationProportion in to money terms.  It gets aggregated with other Payments in to an OutgoingPayment for actual payment to charities.
    """
    def __init__(self, charity, user, amount_GBPennies):
        self.charity = charity
        self.user = user
        self.amount_GBPennies = amount_GBPennies

    def __str__(self):
        return "Payment<\ncharity=%s\nuser=%s\namount_GBPennies=%s\n>" % (self.charity, self.user, self.amount_GBPennies)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.charity == other.charity and self.user == other.user and self.amount_GBPennies == other.amount_GBPennies

    def __hash__(self):
        return hash(self.charity) ^ hash(self.user) ^ hash(self.amount_GBPennies)

class IncomingPayment(db.Model):
    user = db.ReferenceProperty(User)
    amount_GBPennies = db.IntegerProperty()

class OutgoingPayment(db.Model):
    charity = db.ReferenceProperty(Charity)
    amount_GBPennies = db.IntegerProperty()
    status = db.IntegerProperty()

    @classmethod
    def new(cls, **kwargs):
        # TODO: Work out the transactional/consistency semantics of this class, when its lifecycle is better understood
        return OutgoingPayment(**kwargs)

    def __str__(self):
        return "OutgoingPayment<\ncharity=%s\namount_GBPennies=%s\nstatus=%s\n>" % (self.charity, self.amount_GBPennies, self.status)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.charity == other.charity and self.amount_GBPennies == other.amount_GBPennies and self.status == other.status

    def __hash__(self):
        return hash(self.charity) ^ hash(self.amount_GBPennies) ^ hash(self.status)

class OutgoingPaymentState:
    DISPLAYED = 1  # Indicates a payment has been shown on a screen, so someone may be actioning it
    VALUE_MISMATCH = 2  # Indicates a mismatch between incoming payments, and outgoing payments, leading to this payment not being ready to be sent
