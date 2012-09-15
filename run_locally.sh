#!/bin/sh
./generate_app_yaml.py test
export PYTHONPATH=src
lib/sdks/google_appengine/google_appengine/dev_appserver.py --skip_sdk_update_check --port=8080 src
rm src/app.yaml
