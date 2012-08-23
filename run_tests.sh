#!/bin/sh
tests=$(find src -name "*_test.py" | sed -e 's#/#.#g' -e 's#\.py$##g' | sed -e 's#^src\.##g')
PYTHONPATH="src:lib/sdks/google_appengine_1.7.1/google_appengine:$PYTHONPATH" python -m unittest $tests
