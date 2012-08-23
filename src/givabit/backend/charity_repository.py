from charity import Charity
from errors import MissingValueException, MultipleValueException

class CharityRepository(object):
    def list_charities(self):
        return [charity for charity in Charity.all().run()]

    def add_or_update_charity(self, charity):
        charity.put()

    def get_charity(self, name):
        charities = [charity for charity in Charity.all().filter('name =', name).run()]
        count = len(charities)
        if count == 1:
            return charities[0]
        elif count == 0:
            raise MissingValueException('Could not find name=charity %s' % name)
        elif count > 1:
            raise MultipleValueException('Expected one charity to be returned, but got multiple', charities)
