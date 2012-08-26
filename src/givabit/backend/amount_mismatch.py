class AmountMismatch(object):
    def __init__(self, user, incoming_GBPennies, outgoing):
        self.user = user
        self.incoming_GBPennies = incoming_GBPennies
        self.outgoing = frozenset(outgoing)

    def __str__(self):
        return 'AmountMismatch<\nuser=%s\nincoming_GBPennies=%s\noutgoing=%s\n>' % (self.user, self.incoming_GBPennies, self.outgoing)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.user == other.user and self.incoming_GBPennies == other.incoming_GBPennies and self.outgoing == other.outgoing

    def __hash__(self):
        return hash(self.user) ^ hash(self.incoming_GBPennies) ^ hash(self.outgoing)

class AccumulatingMismatchNotifier(object):
    def __init__(self):
        self.accumulated = set([])  # set(AmountMismatch)

    def notify(self, mismatch):
        self.accumulated.add(mismatch)
