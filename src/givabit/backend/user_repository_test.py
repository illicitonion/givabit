import test_utils

from user import User, UserStatus
from user_repository import UserRepository

class UserRepositoryTest(test_utils.TestCase):
    def testValidatesProperties(self):
        self.assertRaises(lambda: User(email='foo'))

    def testCreatesUnconfirmedUser(self):
        email = 'someone@foo.com'
        repo = UserRepository()
        new_user = User(email=email)

        repo.create_unconfirmed_user(new_user)
        self.assertRaises(lambda: repo.get_user(email))
        returned_user = repo.get_unconfirmed_user(email)
        self.assertEquals(returned_user.email, email)
        self.assertEquals(returned_user.status, UserStatus.UNCONFIRMED)

    def testConfirmsUser(self):
        email = 'someone@foo.com'
        repo = UserRepository()
        new_user = User(email=email)

        repo.create_unconfirmed_user(new_user)
        self.assertRaises(lambda: repo.confirm_user(new_user, 'wrong_code'))

        confirmation_code = new_user.confirmation_code
        repo.confirm_user(new_user, confirmation_code)
        self.assertEquals(repo.get_user(email), new_user)

        self.assertRaises(lambda: repo.confirm_user(new_user, confirmation_code))
