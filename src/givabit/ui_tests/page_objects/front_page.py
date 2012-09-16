from givabit.ui_tests.page_objects.base_page_object import BasePageObject
from givabit.ui_tests.page_objects.signup_page import SignupPage

class FrontPage(BasePageObject):
    def __init__(self, driver, base_url):
        BasePageObject.__init__(self, driver, base_url, ('index',))

    def click_signup_link(self):
        self.driver.find_element_by_link_text('Sign up').click()
        return SignupPage(self.driver, self.base_url)
