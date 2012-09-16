import time

from givabit.ui_tests import ui_test_utils
from givabit.ui_tests.page_objects.confirmation_page import ConfirmationPage
from givabit.ui_tests.page_objects.front_page import FrontPage
from givabit.ui_tests.page_objects.login_page import LoginPage, TestUser
from givabit.ui_tests.page_objects.signup_page import SignupPage

from givabit.backend.user import User

from selenium import webdriver

from google.appengine.ext import testbed

class SignupTest(ui_test_utils.TestCase):
    def test_can_sign_up(self):
        test_user = TestUser('%s@foo.com' % self.get_random_value(), self.get_random_value())

        front_page = FrontPage(self.driver, self.get_base_url()).load()
        signup_page = front_page.click_signup_link()
        signup_page.sign_up(test_user)

        user = self.user_repo.get_unconfirmed_user(email=test_user.email)

        confirmation_page = ConfirmationPage(self.driver, self.get_base_url(), user).load()
        confirmation_page.set_password(test_user.password)

        self.assertEquals(len(self.session_repo.get_sessions(email=test_user.email)), 1)
