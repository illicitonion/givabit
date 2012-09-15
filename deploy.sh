#!/bin/bash
dir=$(dirname $0)
${dir}/generate_app_yaml.py staging
${dir}/lib/sdks/google_appengine/google_appengine/appcfg.py update ${dir}/src

rm ${dir}/src/app.yaml
