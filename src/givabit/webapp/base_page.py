import os
import webapp2

from givabit.webapp.template_cache import TemplateCache
from givabit.webapp.url import Url

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=TemplateCache(FileSystemLoader(os.path.abspath(os.path.join(__file__, '..', 'templates')))))
url = Url()

class BasePage(webapp2.RequestHandler):
    def _render_template(self, template_name, data):
        template = env.get_template('%s.html' % template_name)
        return template.render(data)

    def _write_html(self, response, html):
        response.headers['Content-Type'] = 'text/html'
        response.out.write(html)

    def write_template(self, template_name, data=None):
        if data is None:
            data = {}
        data['URL'] = url
        self._write_html(self.response, self._render_template(template_name, data))
