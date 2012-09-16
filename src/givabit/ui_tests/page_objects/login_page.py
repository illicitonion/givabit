from givabit.ui_tests.page_objects.base_page_object import BasePageObject

class TestUser(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginPage(BasePageObject):
    def __init__(self, driver, base_url):
        BasePageObject.__init__(self, driver, base_url, ('login',))

    def login(self, email, password):
        self.set_value(self.driver.find_element_by_id('email'), email)
        self.set_value(self.driver.find_element_by_id('passwd'), password)
        self.driver.find_element_by_id('login-button').click()
