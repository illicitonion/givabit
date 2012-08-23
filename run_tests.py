#!/usr/bin/env python
import sys
sys.path.append('lib/sdks/google_appengine_1.7.1/google_appengine')

import dev_appserver
import unittest

dev_appserver.fix_sys_path()

suites = unittest.loader.TestLoader().discover("src/givabit", pattern="*_test.py")
unittest.TextTestRunner(verbosity=1).run(suites)
