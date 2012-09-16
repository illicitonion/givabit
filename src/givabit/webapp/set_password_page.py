from givabit.backend.user_repository import UserRepository
from givabit.backend.session_repository import SessionRepository
from givabit.webapp.base_page import BasePage

class SetPasswordPage(BasePage):
    def post(self):
        user_repo = UserRepository()
        session_repo = SessionRepository(user_repo=user_repo)

        user_repo.set_password(
            email=self.request.POST['email'],
            password=self.request.POST['password'],
            confirmation_code=self.request.POST['confirmation_code'])

        session = session_repo.log_in(
            email=self.request.POST['email'],
            password=self.request.POST['password'])

        response = self.redirect('/')
        response.set_cookie('sessionid', session.id, httponly=True)
        return response
