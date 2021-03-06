#!/usr/bin/env python

from intmaniac.testrun import Testrun
from intmaniac import tools

import unittest
from os import getcwd


configs = [
    [
        "full-config",
        {
            'meta': {'docker_compose_template': '/tmpl.dat'},
            'environment': {'wohoo': 'hoowoo'},
        },
    ],
    [
        "empty-config",
        {},
    ],
    [
        "default-config",
        {'meta': {'docker_compose_template': '/tmpl.dat'}},
    ],
    [
        "basedir-set-config",
        {'meta': {
            'test_basedir': '/mybasedir',
            'docker_compose_template': '/tmpl.yml',
        }},
    ],
]


class TTestrun(unittest.TestCase):

    def setUp(self):
        tools.enable_debug()

    def test_object_creation_works(self):
        """Check if no errors appear on calling the constructor"""
        for config in configs:
            t = Testrun(*config)
            self.assertEqual(t.name, config[0])

    def test_basedir_setting(self):
        """Check if the 'test_basedir' configuration is correctly evaluated"""
        config = configs[3]
        t = Testrun(*config)
        self.assertEqual(1, len(t.test_env))
        self.assertEqual('/mybasedir/basedir-set-config', t.test_env['test_dir'])

    def test_path_extraction_with_configfile_key(self):
        """Check if all paths are calculated correctly"""
        # nothing specified
        args = {'meta': {'_configfile': '/test/booyah'}}
        t = Testrun("testname", args)
        self.assertEqual('/test/docker-compose.yml.tmpl', t.template)
        self.assertEqual('docker-compose.yml.tmpl', t.template_name)
        self.assertEqual('/test', t.base_dir)
        self.assertEqual('/test/testname', t.test_dir)
        # relative basedir, absolute template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': './td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/t0/td', t.base_dir)
        self.assertEqual('/t0/td/testname', t.test_dir)
        # absolute basedir, relative template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': '/td',
                         'docker_compose_template': 'tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('/t0/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)
        # absolute basedir, absolute template dir
        args = {'meta': {'_configfile': '/t0/conf',
                         'test_basedir': '/td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)

    def test_path_extraction_without_configfile_key(self):
        """Check if all paths are calculated correctly"""
        cdir = getcwd()
        # nothing specified
        args = {'meta': {}}
        t = Testrun("testname", args)
        self.assertEqual('%s/docker-compose.yml.tmpl' % cdir, t.template)
        self.assertEqual('docker-compose.yml.tmpl', t.template_name)
        self.assertEqual('%s' % cdir, t.base_dir)
        self.assertEqual('%s/testname' % cdir, t.test_dir)
        # relative basedir, absolute template dir
        args = {'meta': {'test_basedir': './td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('%s/td' % cdir, t.base_dir)
        self.assertEqual('%s/td/testname' % cdir, t.test_dir)
        # absolute basedir, relative template dir
        args = {'meta': {'test_basedir': '/td',
                         'docker_compose_template': 'tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('%s/tmpl' % cdir, t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)
        # absolute basedir, absolute template dir
        args = {'meta': {'test_basedir': '/td',
                         'docker_compose_template': '/tmpl'}}
        t = Testrun("testname", args)
        self.assertEqual('/tmpl', t.template)
        self.assertEqual('tmpl', t.template_name)
        self.assertEqual('/td', t.base_dir)
        self.assertEqual('/td/testname', t.test_dir)


if __name__ == "__main__":
    unittest.main()
