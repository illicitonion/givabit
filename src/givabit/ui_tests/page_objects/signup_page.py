from givabit.ui_tests.page_objects.base_page_object import BasePageObject

class SignupPage(BasePageObject):
    def __init__(self, driver, base_url):
        BasePageObject.__init__(self, driver, base_url, ('signup',))

    def sign_up(self, user):
        self.set_value(self.driver.find_element_by_id('email'), user.email)
        self.driver.find_element_by_id('signup').click()
