from givabit.backend.user_repository import UserRepository
from givabit.backend.session_repository import SessionRepository

from givabit.webapp.base_page import BasePage

class ConfirmationPage(BasePage):
    def __init__(self, request, response, user_repository=None):
        BasePage.__init__(self, request, response)
        self.user_repository = user_repository if user_repository is not None else UserRepository()

    def get(self):
        GET = self.request.GET
        if not ('email' in GET and 'confirmation_code' in GET):
            self.write_template('confirmation', {'title': 'Givabit - Confirmation', 'success': False, 'error': 'Bad link'})
            return
        email = GET['email']
        confirmation_code = GET['confirmation_code']
        try:
            self.user_repository.confirm_user(email, confirmation_code)
            self.write_template('confirmation', {'title': 'Givabit - Confirmation', 'success': True, 'confirmation_code': confirmation_code, 'email': email})
        except:
            self.write_template('confirmation', {'title': 'Givabit - Confirmation', 'success': False, 'error': 'Confirmation'})
