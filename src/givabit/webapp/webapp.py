import webapp2

from givabit.webapp import confirmation_page
from givabit.webapp import index_page
from givabit.webapp import login_page
from givabit.webapp import set_password_page
from givabit.webapp import signup_page
from givabit.webapp import view_charity_page

page_mapping = [
    ('/login', login_page.LoginPage),
    ('/signup', signup_page.SignupPage),
    (r'/charity/(.+)', view_charity_page.ViewCharityPage),
    ('/confirmation', confirmation_page.ConfirmationPage),
    ('/user/password', set_password_page.SetPasswordPage),
    ('/.*', index_page.IndexPage),
]

app = webapp2.WSGIApplication(page_mapping, debug=True)
