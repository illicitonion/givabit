from givabit.ui_tests.page_objects.base_page_object import BasePageObject

class ConfirmationPage(BasePageObject):
    def __init__(self, driver, base_url, user):
        BasePageObject.__init__(self, driver, base_url, ('confirmation', {'confirmation_code': user.confirmation_code, 'email': user.email}))
        self.user = user

    def set_password(self, password):
        self.set_value(self.driver.find_element_by_id('password'), password)
        self.set_value(self.driver.find_element_by_id('password_confirm'), password)
        self.driver.find_element_by_id('set_password').click()
