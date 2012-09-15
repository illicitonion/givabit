import webapp2

from givabit.backend.user import User
from givabit.backend.user_repository import UserRepository
from givabit.backend.session_repository import SessionRepository

from google.appengine.ext.webapp.util import run_wsgi_app

class LoginPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("""<!DOCTYPE html>
<html>
  <head>
    <title>Givabit - Log in</title>
  </head>
  <body>
    <form action="/login" method="POST">
      <div>
        <input type="email" id="email" name="email" />
        <input type="passwd" id="passwd" name="passwd" />
        <input type="submit" id="login-button" value="Log in" />
      </div>
    </form>
  </body>
</html>""")

    def post(self):
        session = SessionRepository(UserRepository()).log_in(
            email=self.request.POST['email'],
            password=self.request.POST['passwd'])
        response = self.redirect('/')
        response.set_cookie('sessionid', session.id, httponly=True)
        return response
                

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

app = webapp2.WSGIApplication(
        [
            ('/login', LoginPage),
            ('/.*', MainPage)
        ],
        debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
