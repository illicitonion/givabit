import unittest

from givabit.webapp.template_cache import TemplateCache

class TemplateCacheTest(unittest.TestCase):
    class RecordingLoader(object):
        def __init__(self):
            self.loaded = {}

        def get_source(self, environment, template):
            self.loaded[template] = self.loaded.setdefault(template, 0) + 1

    def setUp(self):
        self.recording_loader = TemplateCacheTest.RecordingLoader()

    def test_loads_templates(self):
        template_cache = TemplateCache(self.recording_loader)
        template_cache.get_source(None, 'a')
        template_cache.get_source(None, 'b')
        self.assertEquals(self.recording_loader.loaded['a'], 1)
        self.assertEquals(self.recording_loader.loaded['b'], 1)

    def test_does_not_reload_template(self):
        template_cache = TemplateCache(self.recording_loader)
        template_cache.get_source(None, 'a')
        template_cache.get_source(None, 'a')
        self.assertEquals(self.recording_loader.loaded['a'], 1)
