from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()
    status = db.IntegerProperty()
    confirmation_code = db.StringProperty()

    def __str__(self):
        try:
            key = self.key()
        except db.NotSavedError:
            key = 'NONE'
        return 'User<\nemail=%s\nstatus=%s\nkey=%s\n>' % (self.email, self.status if hasattr(self, 'status') else 'NONE', key)

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())

class UserStatus:
    VALID = 1
    UNCONFIRMED = 2
