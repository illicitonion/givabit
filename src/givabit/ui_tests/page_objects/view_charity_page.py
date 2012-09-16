from givabit.ui_tests.page_objects.base_page_object import BasePageObject

class ViewCharityPage(BasePageObject):
    def __init__(self, driver, base_url, charity, include_charity_name=True):
        charity_id = charity.key().id()
        if include_charity_name:
            charity_identifier = '%s-%s' % (charity_id, charity.name)
        else:
            charity_identifier = charity_id
        BasePageObject.__init__(self, driver, base_url, ('view_charity', {'charity_identifier': charity_identifier}))
        self.charity = charity

    def without_charity_name_in_url(self):
        return ViewCharityPage(self.driver, self.base_url, self.charity, False)

    @property
    def title(self):
        return self.driver.title
