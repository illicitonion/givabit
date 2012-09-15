import hashlib
import os
import uuid

from givabit.backend.errors import IllegalArgumentException, IllegalStateException, MissingValueException, MultipleValueException
from givabit.backend.user import Password, User, UserStatus
from givabit.backend.utils import transactionally

from google.appengine.ext import db

#TODO: Throttle attempts by source and account
#TODO: bcrypt/similar

class IncorrectConfirmationCodeException(Exception):
    pass

class BadLoginException(Exception):
    pass

class UserRepository(object):
    def create_unconfirmed_user(self, user):
        # Creates a user whose account cannot be used without confirmation
        user.status = UserStatus.UNCONFIRMED
        user.confirmation_code = self._generate_confirmation_code()
        user.put()

    def create_confirmed_user_FOR_TEST(self, user):
        user.status = UserStatus.VALID
        user.put()

    def confirm_user(self, user, code):
        found_user = self.get_unconfirmed_user(user.email)
        if not hasattr(user, 'confirmation_code') or user.confirmation_code is None:
            raise IllegalArgumentException('Cannot re-confirm already-confirmed user %s' % user)
        if found_user.confirmation_code == code:
            user.status = UserStatus.VALID
            user.put()
        else:
            raise IncorrectConfirmationCodeException('Could not confirm user %s with code %s' % (user, code))

    def get_unconfirmed_user(self, email):
        # Gets a user whose account is not currently active
        return self._get_user(email=email)

    def get_user(self, email):
        # Gets a user whose account is currently active
        return self._get_user(email, lambda q: q.filter('status =', UserStatus.VALID))

    def set_password(self, email, password, confirmation_code=None, old_password=None):
        user = None
        if confirmation_code is not None:
            user = self.get_unconfirmed_user(email=email)
            self.confirm_user(user=user, code=confirmation_code)
        elif old_password is not None:
            user = self.authenticate(email=email, password=old_password)

        if user is None:
            raise IllegalArgumentException('Must provide either confirmation code or existing password to change password for user %s' % user)

        salt = self._generate_salt()
        user.confirmation_code = None
        user.put()

        def update_password():
            db.delete([p for p in Password.all().ancestor(user).run()])
            Password.new(email=email, salt=salt, hash=self._hash(password, salt), user=user).put()
        transactionally(update_password)

    def authenticate(self, email, password):
        stored = Password.all().filter('email =', email).get()
        if stored is None:
            raise BadLoginException('No user with email %s present' % email)
        if self._hash(password, stored.salt) == stored.hash:
            return stored.user
        raise BadLoginException('Incorrect password for email %s' % email)

    def _generate_salt(self):
        return os.urandom(18).encode('base_64').strip()

    def _generate_confirmation_code(self):
        return str(uuid.uuid4())

    def _hash(self, password, salt):
        return hashlib.sha512(password + salt).hexdigest()

    def _get_user(self, email, filter=None):
        # filter : lambda (query -> query)
        if filter is None:
            filter = lambda f: f
        users = [user for user in filter(User.all().filter('email =', email)).run()]
        count = len(users)
        if count == 1:
            return users[0]
        elif count == 0:
            raise MissingValueException('Could not find user email=%s' % email)
        elif count > 1:
            raise MultipleValueException('Expected one user to be returned, but got multiple', users)
