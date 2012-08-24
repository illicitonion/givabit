from charity import Charity
from google.appengine.ext import db
from user import User

class Payment(db.Model):
    """Represents a payment from a user to a charity.

    This payment is a translation of a DonationProportion in to money terms.  It gets aggregated with other Payments in to an OutgoingPayment for actual payment to charities.  It is also reported to a user as a historical payment they have made.

    The primary reason for this class is to build a strongly-consistent secondary index, aggregating payments by charity (as the primary strongly-consistent index aggregates by user).  The idea is: The common case for wanting to create, update or delete parts of donations is for a user to be editing their preferences, so that is an importantly strongly-consistent group; a more rare, and less time-sensitive case (but needing strong consistency) is calculating outgoing payments; having this strongly-consistently indexed by charity makes the process a whole lot easier, at the cost of transactional double writes on edits.

    Payment's constructor should never be called directly, rather the Payment.new static factory should always be used.
    """
    charity = db.ReferenceProperty(Charity)
    user = db.ReferenceProperty(User)
    amount_GBPennies = db.IntegerProperty()

    @classmethod
    def new(cls, charity, **kwargs):
        return Payment(parent=charity, charity=charity, **kwargs)

class IncomingPayment(db.Model):
    user = db.ReferenceProperty(User)
    amount_GBPennies = db.IntegerProperty()

class OutgoingPayment(db.Model):
    charity = db.ReferenceProperty(Charity)
    amount_GBPennies = db.IntegerProperty()

    @classmethod
    def new(cls, **kwargs):
        # TODO: Work out the transactional/consistency semantics of this class, when its lifecycle is better understood
        return OutgoingPayment(**kwargs)

    def __str__(self):
        return "OutgoingPayment<\ncharity=%s\namount_GBPennies=%s\n>" % (self.charity, self.amount_GBPennies)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.charity == other.charity and self.amount_GBPennies == other.amount_GBPennies

    def __hash__(self):
        return hash(self.charity) ^ hash(self.amount_GBPennies)

class OutgoingPaymentState:
    DISPLAYED = 1  # Indicates a payment has been shown on a screen, so someone may be actioning it
