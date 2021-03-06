from givabit.backend.charity import Charity
from givabit.backend.errors import MissingValueException, MultipleValueException

from google.appengine.api.datastore_errors import BadKeyError

class CharityRepository(object):
    def list_charities(self):
        return [charity for charity in Charity.all().run()]

    def add_or_update_charity(self, charity):
        charity.put()

    def get_charity(self, name=None, id=None):
        if id is not None:
            try:
                charity = Charity.get_by_id(id)
                if charity is None:
                    raise MissingValueException('Could not find charity id=%s' % id)
                return charity
            except BadKeyError:
                raise MissingValueException('Could not find charity id=%s' % id)

        query = Charity.all()
        if name is not None:
            query = query.filter('name =', name)
        charities = [charity for charity in query.run()]
        count = len(charities)
        if count == 1:
            return charities[0]
        elif count == 0:
            raise MissingValueException('Could not find charity name=%s' % name)
        elif count > 1:
            raise MultipleValueException('Expected one charity to be returned, but got multiple', charities)
