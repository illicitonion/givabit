from givabit.backend.user import User
from givabit.backend.user_repository import UserRepository
from givabit.webapp.base_page import BasePage

class SignupPage(BasePage):
    def __init__(self, request, response, user_repository=None):
        BasePage.__init__(self, request, response)
        self.user_repo = user_repository if user_repository is not None else UserRepository()

    def get(self):
        self.write_template('signup', {'title': 'Givabit - Sign up'})

    def post(self):
        POST = self.request.POST
        email = POST['email']
        user = User(email=email)

        self.user_repo.create_unconfirmed_user(user=user, send_email=True)

        response = self.redirect('/signedup')
        return response

