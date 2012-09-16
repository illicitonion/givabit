from givabit.backend.errors import AlreadyExistsException, IllegalArgumentException, MissingValueException
from givabit.backend.user import User, UserStatus
from givabit.backend.user_repository import BadLoginException, IncorrectConfirmationCodeException

from givabit.test_common import test_utils

class UserRepositoryTest(test_utils.TestCase):
    def test_creates_unconfirmed_user(self):
        email = 'someone@foo.com'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        with self.assertRaises(MissingValueException):
            self.user_repo.get_user(email)
        returned_user = self.user_repo.get_unconfirmed_user(email)
        self.assertEquals(returned_user.email, email)
        self.assertEquals(returned_user.status, UserStatus.UNCONFIRMED)

    def test_cannot_create_two_users_with_same_email(self):
        email = 'someone@foo.com'
        user = User(email=email)
        self.user_repo.create_unconfirmed_user(user)

        user2 = User(email=email)
        with self.assertRaises(AlreadyExistsException):
            self.user_repo.create_unconfirmed_user(user2)

    def test_confirms_user(self):
        email = 'someone@foo.com'
        new_user = User(email=email)

        self.user_repo.create_unconfirmed_user(new_user)
        with self.assertRaises(IncorrectConfirmationCodeException):
            self.user_repo.confirm_user(email=email, confirmation_code='wrong_code')

        confirmation_code = new_user.confirmation_code
        self.user_repo.confirm_user(email=email, confirmation_code=confirmation_code)
        self.assertEquals(self.user_repo.get_user(email), new_user)

    def test_cannot_log_in_if_unconfirmed(self):
        email = 'someone@foo.com'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        with self.assertRaises(BadLoginException):
            self.user_repo.authenticate(email=email, password='')

    def test_cannot_log_in_if_password_not_set(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        self.user_repo.confirm_user(email=email, confirmation_code=new_user.confirmation_code)
        with self.assertRaises(BadLoginException):
            self.user_repo.authenticate(email=email, password='')

    def test_preserves_confirmation_code_until_password_set(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.confirm_user(email=email, confirmation_code=new_user.confirmation_code)
        self.user_repo.confirm_user(email=email, confirmation_code=new_user.confirmation_code)

        self.user_repo.set_password(email=new_user.email, password=password, confirmation_code=new_user.confirmation_code)
        self._assert_can_log_in(new_user, password)

    def test_cannot_set_password_with_wrong_second_confirmation(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.confirm_user(email=email, confirmation_code=new_user.confirmation_code)
        self.user_repo.confirm_user(email=email, confirmation_code=new_user.confirmation_code)

        with self.assertRaises(IncorrectConfirmationCodeException):
            self.user_repo.set_password(email=new_user.email, password=password, confirmation_code='wrong')

    def test_can_log_in(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.set_password(email=new_user.email, password=password, confirmation_code=new_user.confirmation_code)
        self._assert_can_log_in(new_user, password)

    def test_users_probably_get_different_safe_salt(self):
        salts = set()
        for _ in range(1000):
            salt = self.user_repo._generate_salt()
            self.assertNotIn('\n', salt)
            salts.add(salt)
        self.assertGreaterEqual(len(salts), 999)

    def test_sequential_users_probably_get_different_confirmation_codes(self):
        confirmation_codes = set()
        for _ in range(1000):
            confirmation_codes.add(self.user_repo._generate_confirmation_code())
        self.assertGreaterEqual(len(confirmation_codes), 999)

    def test_cannot_set_password_without_confirmation_code_if_unconfirmed(self):
        email = 'someone@foo.com'
        password = 'Some_password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        with self.assertRaises(IllegalArgumentException):
            self.user_repo.set_password(email=new_user.email, password=password)

    def test_cannot_set_password_without_existing_password_if_confirmed(self):
        email = 'someone@foo.com'
        old_password = 'Some_password'
        new_password = 'new password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)
        confirmation_code = new_user.confirmation_code

        self.user_repo.set_password(email=new_user.email, password=old_password, confirmation_code=new_user.confirmation_code)
        with self.assertRaises(IllegalArgumentException):
            self.user_repo.set_password(email=new_user.email, password=new_password, confirmation_code=new_user.confirmation_code)
        with self.assertRaises(IllegalArgumentException):
            self.user_repo.set_password(email=new_user.email, password=new_password)
        self._assert_can_log_in(new_user, old_password)

    def test_can_change_password(self):
        email = 'someone@foo.com'
        old_password = 'Some_password'
        new_password = 'Some other password'
        new_user = User(email=email)
        self.user_repo.create_unconfirmed_user(new_user)

        self.user_repo.set_password(email=new_user.email, password=old_password, confirmation_code=new_user.confirmation_code)
        self.user_repo.set_password(email=new_user.email, password=new_password, old_password=old_password)

        with self.assertRaises(BadLoginException):
            self.user_repo.authenticate(email=email, password=old_password)
        self._assert_can_log_in(new_user, new_password)
        

    def _assert_can_log_in(self, user, password):
        found_user = self.user_repo.authenticate(email=user.email, password=password)
        self.assertEquals(found_user, user)

