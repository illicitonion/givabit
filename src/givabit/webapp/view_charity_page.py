from givabit.backend.charity_repository import CharityRepository
from givabit.backend.errors import MissingValueException

from givabit.webapp.base_page import BasePage

class ViewCharityPage(BasePage):
    def __init__(self, request, response):
        BasePage.__init__(self, request, response)

    def get(self, charity_id):
        try:
            id = int(charity_id.split('-')[0])
            charity = CharityRepository().get_charity(id=id)
            self.write_template('view_charity', {'title': 'Givabit - %s' % charity.name, 'charity': charity})
        except (MissingValueException, ValueError):
            self.write_template('view_charity', {'title': 'Givabit - Could not find charity', 'success': False, 'error': 'Could not find charity'})
