import unittest
import uuid

from givabit.backend.user import User
from givabit.email.email_service import EmailService
from givabit.webapp.url import Url

from google.appengine.ext import testbed

class EmailServiceTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def test_user_confirmation_mail_contains_confirmation_code(self):
        confirmation_code = str(uuid.uuid4())
        email = '%s@foo.com' % str(uuid.uuid4())
        user = User(email=email, confirmation_code=confirmation_code)
        EmailService().send_user_confirmation_mail(user)
        
        messages = self.mail_stub.get_sent_messages()
        self.assertEquals(len(messages), 1)
        
        message = messages[0]
        self.assertEquals(message.to, email)
        self.assertIn(Url().for_page('confirmation', confirmation_code=confirmation_code, email=email), str(message.body))
