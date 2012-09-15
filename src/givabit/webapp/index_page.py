from givabit.webapp.base_page import BasePage

class IndexPage(BasePage):
    def get(self):
        self.write_template('index', {'title': 'Givabit'})
