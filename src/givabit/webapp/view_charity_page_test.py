import webapp2

from givabit.test_common import test_utils
from givabit.webapp.view_charity_page import ViewCharityPage
from givabit.webapp.url import Url

class ViewCharityPageTest(test_utils.TestCase):
    def test_missing_key_gives_error(self):
        missing_charity_identifier = '1'
        request = webapp2.Request.blank(Url().for_page('view_charity', include_hostname=False, charity_identifier=missing_charity_identifier))

        response = webapp2.Response()
        ViewCharityPage(request=request, response=response).get(charity_id=missing_charity_identifier)

        self.assertIn('Could not find', response.body)

    def test_non_numeric_key_gives_error(self):
        missing_charity_identifier = 'Oxfam'
        request = webapp2.Request.blank(Url().for_page('view_charity', include_hostname=False, charity_identifier=missing_charity_identifier))

        response = webapp2.Response()
        ViewCharityPage(request=request, response=response).get(charity_id=missing_charity_identifier)

        self.assertIn('Could not find', response.body)
