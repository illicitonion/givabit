from jinja2 import BaseLoader

class TemplateCache(BaseLoader):
    def __init__(self, delegate):
        self._delegate = delegate
        self._cache = {}

    def get_source(self, environment, template):
        if template in self._cache:
            return self._cache[template]
        found_template = self._delegate.get_source(environment, template)
        self._cache[template] = found_template
        return found_template

    def list_templates(self):
        return self._delegate.list_templates()


