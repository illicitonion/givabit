#!/usr/bin/env python
import sys
sys.path.append('lib/sdks/google_appengine_1.7.1/google_appengine')
sys.path.append('src')

import dev_appserver
import unittest

dev_appserver.fix_sys_path()

paths = ['src/givabit/backend', 'src/givabit/email', 'src/givabit/webapp']

suites = unittest.TestSuite()

for path in paths:
    suites.addTests(unittest.loader.TestLoader().discover(path, pattern='*_test.py'))

if len(sys.argv) > 1:
    def GetTestCases(caseorsuite, acc=None):
        if acc is None:
            acc = []
        if isinstance(caseorsuite, unittest.TestCase):
            acc.append(caseorsuite)
            return acc
        for child in caseorsuite:
            GetTestCases(child, acc)
        return acc
    all_tests = GetTestCases(suites)
    tests = [test for test in all_tests if sys.argv[1] in test.id()]
    suites = unittest.TestSuite(tests)

unittest.TextTestRunner(verbosity=1).run(suites)
