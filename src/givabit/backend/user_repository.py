from user import User, UserStatus
from errors import IllegalStateException, MissingValueException, MultipleValueException

class UserRepository(object):
    def create_unconfirmed_user(self, user):
        # Creates a user whose account cannot be used without confirmation
        user.status = UserStatus.UNCONFIRMED
        user.confirmation_code = 'some code'
        user.put()

    def confirm_user(self, user, code):
        found_user = self.get_unconfirmed_user(user.email)
        if not hasattr(user, 'confirmation_code') or user.confirmation_code is None:
            raise IllegalStateException('Cannot re-confirm already-confirmed user %s' % user)
        if found_user.confirmation_code == code:
            user.status = UserStatus.VALID
            user.confirmation_code = None
            user.put()

    def get_unconfirmed_user(self, email):
        # Gets a user whose account is not currently active
        return self._get_user(email, lambda q: q.filter('status =', UserStatus.UNCONFIRMED))

    def get_user(self, email):
        # Gets a user whose account is currently active
        return self._get_user(email, lambda q: q.filter('status =', UserStatus.VALID))

    def _get_user(self, email, filter):
        # filter : lambda (query -> query)
        users = [user for user in filter(User.all().filter('email =', email)).run()]
        count = len(users)
        if count == 1:
            return users[0]
        elif count == 0:
            raise MissingValueException('Could not find user email=%s' % email)
        elif count > 1:
            raise MultipleValueException('Expected one user to be returned, but got multiple', users)
