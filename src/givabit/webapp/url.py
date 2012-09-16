import os

from string import Template

PATHS = {
         'index': Template('/'),
         'login': Template('/login'),
         'confirmation': Template('/confirmation?email=${email}&confirmation_code=${confirmation_code}'),
         'signup': Template('/signup'),
        }

BASE_URL = os.environ['BASE_URL'] if 'BASE_URL' in os.environ else 'https://givabit-dev.appspot.com'

class Url(object):
    def for_page(self, page, include_hostname=False, **kwargs):
        if not page in PATHS:
            raise Exception('Did not know how to link to page \'%s\', knew: %s' % (page, PATHS.keys()))
        path = PATHS[page].substitute(**kwargs)
        if include_hostname:
            return '%s%s' % (BASE_URL, path)
        return path
