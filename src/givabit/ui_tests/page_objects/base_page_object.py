from givabit.webapp.url import Url

class BasePageObject(object):
    def __init__(self, driver, base_url, pathspec):
        # pathspec = (pagename, {param: value})
        self.driver = driver
        self.base_url = base_url
        self.url = Url().for_page(pathspec[0], include_hostname=True, **(pathspec[1] if len(pathspec) > 1 else {}))

    def load(self):
        self.driver.get(self.url)
        return self

    def set_value(self, field, value):
        field.clear()
        field.send_keys(value)
