import time

from givabit.ui_tests import ui_test_utils
from givabit.ui_tests.page_objects.login_page import LoginPage

from givabit.backend.user import User

from selenium import webdriver

from google.appengine.ext import testbed

class LoginTest(ui_test_utils.TestCase):
    def setUp(self):
        super(LoginTest, self).setUp()
        self.user = self.create_ready_to_use_user()

    def test_can_log_in(self):
        login_page = LoginPage(self.driver, self.get_base_url()).load()
        login_page.login(self.user.email, self.user.password)

        self._assert_only_session_for_user(self.user, self.get_session_id())

    def test_cookies_are_http_only(self):
        login_page = LoginPage(self.driver, self.get_base_url()).load()
        login_page.login(self.user.email, self.user.password)
        self.assertEquals(self.execute_javascript('return document.cookie;'), '')

    def _assert_only_session_for_user(self, user, session_id):
        sessions = self.session_repo.get_sessions(email=user.email)
        session_ids = set([session.id for session in sessions])
        self.assertSetEqual(session_ids, set([session_id]))

    def get_session_id(self):
        return self.get_cookie('sessionid')['value']
