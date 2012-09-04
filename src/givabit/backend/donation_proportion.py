from givabit.backend.charity import Charity
from givabit.backend.user import User

from google.appengine.ext import db

class DonationProportion(db.Model):
    """ Represents a proportion of a donation to a charity by a user.

    The amount is a unitless value, which when taken as the numerator over the sum of all proportions for that user, gives a fraction of their total donation that should go to this charity.  An amount is only a relevant measure of magnitude compared to the same user's other donation proportions; comparisons with other users' amounts don't make sense.

    This class should be constructed using its factory new method, not with its constructor.
    """
    user = db.ReferenceProperty(User)
    charity = db.ReferenceProperty(Charity)
    amount = db.IntegerProperty()

    @classmethod
    def new(cls, user, **kwargs):
        return cls(parent=user, user=user, **kwargs)

    def __str__(self):
        return 'DonationProportion<\nuser=%s\ncharity=%s\namount=%s>' % (self.user, self.charity, self.amount)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.key() == other.key()
