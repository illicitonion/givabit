from givabit.backend.session import Session
from givabit.backend.session_repository import SessionRepository
from givabit.backend.user_repository import BadLoginException

from givabit.test_common import test_utils

class SessionRepositoryTest(test_utils.TestCase):
    def setUp(self):
        super(SessionRepositoryTest, self).setUp()
        self.user = self.create_ready_to_use_user()
        self.email = self.user.email
        self.password = self.user.password

    def test_logging_in_creates_session(self):
        sessions_before = self.session_repo.get_sessions(email=self.email)
        self.session_repo.log_in(email=self.email, password=self.password)
        sessions_after = self.session_repo.get_sessions(email=self.email)

        self.assertEquals(len(sessions_after.difference(sessions_before)), 1)

    def test_incorrect_login_does_not_create_session(self):
        wrong_password = self.password + 'z'

        sessions_before = self.session_repo.get_sessions(email=self.email)
        with self.assertRaises(BadLoginException):
            self.session_repo.log_in(email=self.email, password=wrong_password)
        sessions_after = self.session_repo.get_sessions(email=self.email)

        self.assertSetEqual(sessions_after, sessions_before)

    def test_session_user_is_logged_in_user(self):
        self.session_repo.log_in(email=self.email, password=self.password)
        sessions = self.session_repo.get_sessions(email=self.email)
        self.assertEquals(len(sessions), 1)
        self.assertEquals(sessions.pop().user, self.user_repo.get_user(email=self.email))

    def test_two_logins_get_different_session_ids(self):
        for _ in range(100):
            self.session_repo.log_in(email=self.email, password=self.password)
        session_ids = set([session.id for session in self.session_repo.get_sessions(email=self.email)])
        self.assertEquals(len(session_ids), 100)
