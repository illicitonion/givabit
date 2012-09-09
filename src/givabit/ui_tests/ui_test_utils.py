import os
import subprocess
import sys
import time
import unittest

from givabit.test_common import test_utils

from selenium import webdriver

class TestCase(test_utils.TestCase):
    def setUp(self):
        self._start_server()
        self.driver = webdriver.Chrome(executable_path=self._get_chromedriver())

    def _start_server(self):
        self.port = self._pick_unused_port()
        dev_appserver = self._get_path_from_root('lib/sdks/google_appengine/google_appengine/dev_appserver.py')
        basedir = self._get_path_from_root('src/givabit')
        self.dev_appserver = subprocess.Popen([dev_appserver, '--skip_sdk_update_check', '--port=%d' % self.port, basedir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        started = False

        read_stderr = ''
        end_time = time.time() + 5

        while not started and time.time() < end_time:
            line = self.dev_appserver.stderr.readline()
            read_stderr += line
            if 'on port %s' % self.port in line:
                started = True

        if not started:
            print 'Could not start server; stderr from dev_appserver: %s' % read_stderr

    def tearDown(self):
        self.dev_appserver.kill()
        self.driver.quit()

    def _pick_unused_port(self):
        # TODO: Pick an unused port
        return 8080

    def _get_chromedriver(self):
        if sys.platform == 'darwin':
            trailing_path = 'mac'
        else:
            raise Exception('Did not know where chromedriver was for platform: %s' % sys.platform)
        return self._get_path_from_root(os.path.join('lib', 'misc', 'chromedriver', trailing_path))

    def _get_path_from_root(self, file):
        return os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', file))

    def get_base_url(self):
        return 'http://localhost:%s' % self.port
