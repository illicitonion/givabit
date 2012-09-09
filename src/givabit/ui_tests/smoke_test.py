from givabit.ui_tests import ui_test_utils

from selenium import webdriver

class SmokeTest(ui_test_utils.TestCase):
    def test_launches_app(self):
        self.driver.get(self.get_base_url())
        self.assertIn('Hello, webapp World!', self.driver.page_source)
