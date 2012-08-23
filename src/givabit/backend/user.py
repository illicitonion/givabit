from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()
    status = db.IntegerProperty()
    confirmation_code = db.StringProperty()

    def __str__(self):
        return 'User<\nemail=%s\nstatus=%s\n>' % (self.email, self.status if hasattr(self, 'status') else 'NONE')

    def __eq__(self, other):
        return self.key() == other.key()

class UserStatus:
    VALID = 1
    UNCONFIRMED = 2
