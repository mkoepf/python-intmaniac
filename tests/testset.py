#!/usr/bin/env python

import unittest
from runner.testset import Testset
from runner.testrun import Testrun

configs = [
    ('full config', {
        'meta': {'docker_compose_template': '/tmpl.dat'},
        'environment': {'wohoo': 'hoowoo'},
    }),
    ('empty config', {}),
    ('default config', {
        'meta': {'docker_compose_template': '/tmpl.dat'},
    }),
]


class TTestset(unittest.TestCase):

    def test_global_environment_punch(self):
        t = Testset()
        t.set_global_config({'environment': {"ho": "wo"}})
        t.add_from_config("added", {})
        self.assertEqual(1, len(t.tests))
        self.assertEqual('wo', t.tests[0].test_env['ho'])

    def test_environment_defaults(self):
        t = Testrun(*configs[2])
        self.assertEqual(1, len(t.test_env))
        self.assertEqual('/default-config', t.test_env['test_dir'])


if __name__ == "__main__":
    unittest.main()
