import webapp2

from givabit.webapp import index_page
from givabit.webapp import login_page

page_mapping = [
    ('/login', login_page.LoginPage),
    ('/.*', index_page.IndexPage),
]

app = webapp2.WSGIApplication(page_mapping, debug=True)
