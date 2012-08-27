import test_utils

from user import User, UserStatus

class UserRepositoryTest(test_utils.TestCase):
    def test_validates_properties(self):
        self.assertRaises(lambda: User(email='foo'))

    def test_creates_unconfirmed_user(self):
        email = 'someone@foo.com'
        new_user = User(email=email)

        self.user_repo.create_unconfirmed_user(new_user)
        self.assertRaises(lambda: self.user_repo.get_user(email))
        returned_user = self.user_repo.get_unconfirmed_user(email)
        self.assertEquals(returned_user.email, email)
        self.assertEquals(returned_user.status, UserStatus.UNCONFIRMED)

    def test_confirms_user(self):
        email = 'someone@foo.com'
        new_user = User(email=email)

        self.user_repo.create_unconfirmed_user(new_user)
        self.assertRaises(lambda: self.user_repo.confirm_user(new_user, 'wrong_code'))

        confirmation_code = new_user.confirmation_code
        self.user_repo.confirm_user(new_user, confirmation_code)
        self.assertEquals(self.user_repo.get_user(email), new_user)

        self.assertRaises(lambda: self.user_repo.confirm_user(new_user, confirmation_code))
