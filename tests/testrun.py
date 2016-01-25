#!/usr/bin/env python

import unittest
from runner.testrun import Testrun

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
]


class TTestrun(unittest.TestCase):


    def test_object_creation_works(self):
        """Check if no errors appear on calling the constructor"""
        for config in configs:
            t = Testrun(*config['args'], **config['kwargs'])
            self.assertEqual(t.name, config['kwargs']['name'])

    def test_test_dir_construction(self):
        """Check if the test dir path is constructed correctly"""
        config = configs[2]
        t = Testrun(*config['args'], **config['kwargs'])
        self.assertEqual(1, len(t.test_env))
        self.assertEqual('/default-config', t.test_env['test_dir'])


if __name__ == "__main__":
    unittest.main()
