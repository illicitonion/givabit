from givabit.backend.charity import Charity
from givabit.backend.charity_repository import CharityRepository

from givabit.ui_tests import ui_test_utils
from givabit.ui_tests.page_objects.view_charity_page import ViewCharityPage

from selenium import webdriver

class ViewCharityTest(ui_test_utils.TestCase):
    def test_view_charity_urls(self):
        charity = Charity(name='Oxfam')
        CharityRepository().add_or_update_charity(charity)

        view_charity_page = ViewCharityPage(self.driver, self.get_base_url(), charity).load()
        self.assertIn(charity.name, view_charity_page.title)

        view_charity_page.without_charity_name_in_url().load()
        self.assertIn(charity.name, view_charity_page.title)
