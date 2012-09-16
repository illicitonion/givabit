import unittest
import uuid
import webapp2

from givabit.backend.errors import MissingValueException
from givabit.backend.user_repository import UserRepository
from givabit.test_common import test_utils
from givabit.webapp.signup_page import SignupPage
from givabit.webapp.url import Url

class SignupPageTest(test_utils.TestCase):
    def test_signing_up_requires_confirmation(self):
        email = '%s@foo.com' % self.get_random_value()

        self._assert_no_confirmed_user(email=email)
        self._assert_no_unconfirmed_user(email=email)

        request = webapp2.Request.blank('/signup')
        request.method = 'POST'
        request.POST['email'] = email

        SignupPage(request=request, response=webapp2.Response()).post()

        user = self.user_repo.get_unconfirmed_user(email=email)
        self.assertEquals(user.email, email)

        self._assert_no_confirmed_user(email=email)


    def test_sends_email_with_confirmation_link(self):
        email = '%s@foo.com' % self.get_random_value()

        self._assert_no_confirmed_user(email=email)
        self._assert_no_unconfirmed_user(email=email)

        request = webapp2.Request.blank('/signup')
        request.method = 'POST'
        request.POST['email'] = email

        class MockEmailService(object):
            def send_user_confirmation_mail(self, user):
                self.user = user
        email_service = MockEmailService()
        user_repo = UserRepository(email_service=email_service)

        SignupPage(request=request, response=webapp2.Response(), user_repository=user_repo).post()

        user = self.user_repo.get_unconfirmed_user(email=email)
        self.assertEquals(email_service.user, user)

    def test_fails_if_email_already_exists(self):
        pass

    def _assert_no_confirmed_user(self, email):
        with self.assertRaises(MissingValueException) as ctx:
            self.user_repo.get_user(email=email)

    def _assert_no_unconfirmed_user(self, email):
        with self.assertRaises(MissingValueException) as ctx:
            self.user_repo.get_unconfirmed_user(email=email)
