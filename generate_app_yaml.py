#!/usr/bin/env python
import string
import sys

def usage():
    raise Exception('No args passed.  Usage: generate_app_yaml.py {staging,test}')

def get_version(configuration):
    with open('.versions', 'r') as f:
        versions = f.readlines()
        to_return = None
        found_versions = {}
        for line in versions:
            (key,value) = line.strip().split('=')
            if key == configuration:
                value = int(value) + 1
                to_return = value
            found_versions[key] = value

    if to_return is None:
        raise Exception('Could not find version in .versions for configuration: %s, found: %s' % (configuration, found_versions))

    to_write = ''
    for (key,value) in found_versions.items():
        to_write += '%s=%s\n' % (key, value)
    with open('.versions', 'w') as f:
        f.write(to_write[:-1])
    return to_return


if len(sys.argv) != 2:
    usage()
configuration = sys.argv[1]

to_write = """
application: ${application_name}
version: ${version}
runtime: python27
threadsafe: true
api_version: 1

handlers:
- url: /favicon\.ico
  static_files: static/favicon.ico
  upload: static/favicon\.ico

- url: /.*
  script: givabit.webapp.webapp.app
  secure: always
  ${login_pair}

libraries:
- name: jinja2
  version: "2.6"

${config_specific}"""


if configuration == 'staging':
    version = get_version(configuration)
    substitutes = {
                    'application_name': 'givabit-dev',
                    'version': version,
                    'login_pair': 'login: admin',
                    'config_specific': ''
                  }
elif configuration == 'test':
    substitutes = {
                    'application_name': 'givabit-dev',
                    'version': 1,
                    'login_pair': '',
                    'config_specific': """builtins:
- remote_api: on"""
                  }
else:
    usage()

with open('src/app.yaml', 'w') as f:
    f.write(string.Template(to_write).substitute(substitutes))
