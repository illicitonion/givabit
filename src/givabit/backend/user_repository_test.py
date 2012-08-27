import test_utils

from user import User, UserStatus
from user_repository import IncorrectConfirmationCodeException

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

    def test_cannot_log_in_if_unconfirmed(self):
        email = 'someone@foo.com'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        self.assertRaises(lambda: self.user_repo.authenticate(email=email, password=''))

    def test_cannot_log_in_if_password_not_set(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        self.user_repo.confirm_user(new_user, new_user.confirmation_code)
        self.assertRaises(lambda: self.user_repo.authenticate(email=email, password=''))

    def test_preserves_confirmation_code_until_password_set(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.confirm_user(new_user, new_user.confirmation_code)
        self.user_repo.confirm_user(new_user, new_user.confirmation_code)

        self.user_repo.set_password(email=new_user.email, password=password, confirmation_code=new_user.confirmation_code)
        self._assert_can_log_in(new_user, password)

    def test_cannot_set_password_with_wrong_second_confirmation(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.confirm_user(new_user, new_user.confirmation_code)
        self.user_repo.confirm_user(new_user, new_user.confirmation_code)

        self.assertRaises(IncorrectConfirmationCodeException, lambda: self.user_repo.set_password(email=new_user.email, password=password, confirmation_code='wrong'))

    def test_can_log_in(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.set_password(email=new_user.email, password=password, confirmation_code=new_user.confirmation_code)
        self._assert_can_log_in(new_user, password)

    def test_sequential_users_probably_get_different_salt(self):
        pass

    def test_sequential_users_probably_get_different_confirmation_codes(self):
        pass

    def test_cannot_set_password_without_confirmation_code_if_unconfirmed(self):
        pass

    def test_cannot_set_password_without_existing_password_if_confirmed(self):
        pass

    def _assert_can_log_in(self, user, password):
        found_user = self.user_repo.authenticate(email=user.email, password=password)
        self.assertEquals(found_user, user)

