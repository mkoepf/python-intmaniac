#!/usr/bin/env python

from tools import deep_merge

import os.path
import threading
from re import sub as resub
import shutil


default_config = {
    'environment': {},
    'meta': {
        # no default values, must be set in config:
        'test_container': None,
        # default values, always used
        'docker_compose_template': 'docker-compose.yml.tmpl',
        'test_shell': '/bin/bash',
        'run_timeout': 0,
        'test_service': 'test-service',
        # optional values
        'docker_compose_params': None,
        'test_commands': None,
        'test_report_files': None,
    },
}


class Testrun(threading.Thread):
    """Actually invokes docker-compose with the information given in the
    configuration, and evaluates the results.
    """

    def __init__(self, test_definition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_definition = deep_merge(default_config, test_definition)
        # quick shortcuts
        self.test_env = self.test_definition['environment']
        self.test_meta = self.test_definition['meta']
        # start initializing variables - directories and file names
        tmpl = self.test_meta['docker_compose_template']
        self.template = os.path.realpath(tmpl)
        self.base_dir = os.path.dirname(self.template)
        self.test_dir = os.path.join(self.base_dir,
                                     resub("[^a-zA-Z0-9_]", "-", self.name))
        self.template_name = os.path.basename(tmpl)
        # auto-add some variables to environment
        self.test_env['test_dir'] = self.test_dir
        # result evaluation
        self.success = True
        self.report = None

    def __str__(self):
        return "<runner.Test '%s'>" % self.name

    def __repr__(self):
        return self.__str__()

    def init_environment(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        os.mkdir(self.test_dir)
        os.chdir(self.test_dir)
        # TODO - catch & error handling if template cannot be found.
        tpl = open(self.template, "r").read()
        for key, val in self.test_env.items():
            tpl = tpl.replace("%%%%%s%%%%" % key.upper(), val)
        # TODO (maybe) - catch and error handling if new tmpl cannot be written
        open(os.path.join(self.testdir,
                          "docker-compose.yml").write("\n".join(tpl)))

    def run(self):
        self.init_environment()

    def succeeded(self):
        return self.success


if __name__ == "__main__":
    print("Don't do this :)")
