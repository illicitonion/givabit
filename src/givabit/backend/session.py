from givabit.backend.user import User

from google.appengine.ext import db

class Session(db.Model):
    id = db.StringProperty()
    user = db.ReferenceProperty(User)

    def __str__(self):
        return 'Session<\nid=%s\nuser=%s\n>' % (self.id, self.user)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())
