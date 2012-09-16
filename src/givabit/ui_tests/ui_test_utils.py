import os
import subprocess
import sys
import threading
import time
import unittest

from google.appengine.ext.remote_api import remote_api_stub

from givabit.test_common import test_utils
from givabit.webapp import url

from selenium import webdriver

class FileConsumer(threading.Thread):
    def __init__(self, fd):
        threading.Thread.__init__(self)
        self.fd = fd

    def run(self):
        line = True
        while line:
            line = self.fd.readline()

class TestCase(test_utils.TestCase):
    def setUp(self):
        self._start_server()
        self.addCleanup(self.dev_appserver.kill)
        super(TestCase, self).setUp()
        self.driver = webdriver.Chrome(executable_path=self._get_chromedriver())
        if not 'LEAVE_RUNNING' in os.environ:
            self.addCleanup(self.driver.quit)

    def _start_server(self):
        self.port = self._pick_unused_port()
        url.BASE_URL = self.get_base_url()
        dev_appserver = self._get_path_from_root('lib/sdks/google_appengine/google_appengine/dev_appserver.py')
        basedir = self._get_path_from_root('src')
        env = os.environ
        env['PYTHONPATH'] = self._get_path_from_root('src')
        args = [dev_appserver, '--skip_sdk_update_check', '--port=%d' % self.port, '--clear_datastore', basedir]
        self.dev_appserver = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        started = False

        read_stderr = ''
        end_time = time.time() + 5

        while not started and time.time() < end_time:
            line = self.dev_appserver.stderr.readline()
            read_stderr += line
            if 'on port %s' % self.port in line:
                started = True

        if not started:
            raise Exception('Could not start server; stderr from dev_appserver: %s' % read_stderr)

        # Hangs result if output isn't consumed
        FileConsumer(self.dev_appserver.stdout).start()
        FileConsumer(self.dev_appserver.stderr).start()

    def set_up_database(self):
        remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', lambda: ('', ''), 'localhost:%s' % self.port)

    def tear_down_database(self):
        pass

    def _pick_unused_port(self):
        # TODO: Pick an unused port
        return 8080

    def _get_chromedriver(self):
        if sys.platform == 'darwin':
            trailing_path = 'mac'
        elif sys.platform == 'linux2':
            trailing_path = 'linux_32'
        else:
            raise Exception('Did not know where chromedriver was for platform: %s' % sys.platform)
        return self._get_path_from_root(os.path.join('lib', 'misc', 'chromedriver', trailing_path))

    def _get_path_from_root(self, file):
        return os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', file))

    def get_base_url(self):
        return 'http://localhost:%s' % self.port

    def execute_javascript(self, script):
        return self.driver.execute_script(script)

    def get_cookie(self, name):
        return self.driver.get_cookie(name)
