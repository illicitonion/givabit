#!/bin/sh
./generate_app_yaml.py test
export PYTHONPATH=src
export BASE_URL=http://localhost:8080
lib/sdks/google_appengine/google_appengine/dev_appserver.py --skip_sdk_update_check --port=8080 --clear_datastore src
rm src/app.yaml
