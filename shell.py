#!/usr/bin/env python
import sys
sys.path.append('lib/sdks/google_appengine_1.7.1/google_appengine')
sys.path.append('src')

import dev_appserver
dev_appserver.fix_sys_path()

import code
code.interact(local=locals())
