#!/usr/bin/env python

from intmaniac.testrun import Testrun

import unittest
from os import getcwd


configs = [
    {
        'args': (
            {
                'meta': {'docker_compose_template': '/tmpl.dat'},
                'environment': {'wohoo': 'hoowoo'},
            },
        ),
        'kwargs': {"name": "full-config"}
    },
    {
        'args': (
            {},
        ),
        'kwargs': {"name": "empty-config"}
    },
    {
        'args': (
            {'meta': {'docker_compose_template': '/tmpl.dat'}},
        ),
        'kwargs': {"name": "default-config"}
    },
    {
        'args': (
            {'meta': {
                'test_basedir': '/mybasedir',
                'docker_compose_template': '/tmpl.yml',
            }},
        ),
        'kwargs': {"name": "basedir-set-config"}
    },
]


class TTestrun(unittest.TestCase):

    def test_object_creation_works(self):
        """Check if no errors appear on calling the constructor"""
        for config in configs:
            t = Testrun(*config['args'], **config['kwargs'])
            self.assertEqual(t.name, config['kwargs']['name'])

    def test_basedir_setting(self):
        """Check if the 'test_basedir' configuration is correctly evaluated"""
        config = configs[3]
        t = Testrun(*config['args'], **config['kwargs'])
        self.assertEqual(1, len(t.test_env))
        self.assertEqual('/mybasedir/basedir-set-config', t.test_env['test_dir'])

    def test_path_extraction_with_configfile_key(self):
        """Check if all paths are calculated correctly"""
        # nothing specified
        args = {'meta': {'_configfile': '/test/booyah'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/test/docker-compose.yml.tmpl', t.template)
        self.assertEqual('docker-compose.yml.tmpl', t.template_name)
        self.assertEqual('/test', t.base_dir)
        self.assertEqual('/test/testname', t.test_dir)
        # relative basedir, absolute template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': './td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/t0/td', t.base_dir)
        self.assertEqual('/t0/td/testname', t.test_dir)
        # absolute basedir, relative template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': '/td',
                         'docker_compose_template': 'tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/t0/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)
        # absolute basedir, absolute template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': '/td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)

    def test_path_extraction_without_configfile_key(self):
        """Check if all paths are calculated correctly"""
        cdir = getcwd()
        # nothing specified
        args = {'meta': {}}
        t = Testrun(args, name="testname")
        self.assertEqual('%s/docker-compose.yml.tmpl' % cdir, t.template)
        self.assertEqual('docker-compose.yml.tmpl', t.template_name)
        self.assertEqual('%s' % cdir, t.base_dir)
        self.assertEqual('%s/testname' % cdir, t.test_dir)
        # relative basedir, absolute template dir
        args = {'meta': {'test_basedir': './td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('%s/td' % cdir, t.base_dir)
        self.assertEqual('%s/td/testname' % cdir, t.test_dir)
        # absolute basedir, relative template dir
        args = {'meta': {'test_basedir': '/td',
                         'docker_compose_template': 'tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('%s/tmpl' % cdir, t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)
        # absolute basedir, absolute template dir
        args = {'meta': {'test_basedir': '/td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun(args, name="testname")
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)


if __name__ == "__main__":
    unittest.main()
