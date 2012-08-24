from google.appengine.ext import db

class Charity(db.Model):
    name = db.StringProperty()

    def __str__(self):
        return 'Charity<\nname=%s\n>' % (self.name)

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())
