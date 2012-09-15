class TestUser(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginPage(object):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def load(self):
        self.driver.get('%s%s' % (self.base_url, '/login'))
        return self

    def login(self, email, password):
        self.set_value(self.driver.find_element_by_id('email'), email)
        self.set_value(self.driver.find_element_by_id('passwd'), password)
        self.driver.find_element_by_id('login-button').click()

    def set_value(self, field, value):
        field.clear()
        field.send_keys(value)
