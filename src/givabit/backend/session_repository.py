import uuid

from givabit.backend.session import Session

class SessionRepository(object):
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_sessions(self, email):
        user = self.user_repo.get_user(email=email)
        sessions = Session.all().filter('user =', user).run()
        return set(sessions)

    def log_in(self, email, password):
        user = self.user_repo.authenticate(email=email, password=password)
        session = Session(id=str(uuid.uuid4()), user=user)
        session.put()
        return session
