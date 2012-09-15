from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()
    status = db.IntegerProperty()
    confirmation_code = db.StringProperty()
    donation_amount = db.IntegerProperty()

    def __str__(self):
        try:
            key = self.key()
        except db.NotSavedError:
            key = 'NONE'
        return 'User<\nemail=%s\nstatus=%s\nkey=%s\ndonation_amount=%s\n>' % (self.email, self.status if hasattr(self, 'status') else 'NONE', key, self.donation_amount)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())

class UserStatus:
    VALID = 1
    UNCONFIRMED = 2

class Password(db.Model):
    email = db.EmailProperty()
    salt = db.StringProperty()
    hash = db.StringProperty()
    user = db.ReferenceProperty(User)

    @classmethod
    def new(cls, user, **kwargs):
        return Password(parent=user, user=user, **kwargs)

    def __str__(self):
        return 'Password<\nemail=%s\nsalt=%s\nhash=%s\nuser=%s\n>' % (self.email, self.salt, self.hash, self.user)

    def __repr__(self):
        return str(self)
