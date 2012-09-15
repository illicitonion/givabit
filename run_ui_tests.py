#!/usr/bin/env python
import os
os.environ['SKIP_TRANSACTIONS_FOR_TEST'] = 'true'

import sys
sys.path.append('lib/sdks/google_appengine_1.7.1/google_appengine')
sys.path.append('src')

import dev_appserver
import subprocess
import unittest

dev_appserver.fix_sys_path()

suites = unittest.loader.TestLoader().discover("src/givabit/ui_tests", pattern="*_test.py")

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
    tests = [test for test in all_tests if test.id().startswith(sys.argv[1]) or test.id().endswith(sys.argv[1])]
    suites = unittest.TestSuite(tests)

subprocess.check_call(['./generate_app_yaml.py', 'test'])

unittest.TextTestRunner(verbosity=1).run(suites)

subprocess.check_call(['rm', 'src/app.yaml'])
