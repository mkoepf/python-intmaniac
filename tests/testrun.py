#!/usr/bin/env python

import unittest
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


class TTestrun(unittest.TestCase):
    def test_config_constructor(self):
        for config in configs:
            Testrun(*config)

    def test_environment_defaults(self):
        t = Testrun(*configs[2])
        self.assertEqual(1, len(t.test_env))
        self.assertEqual('/default-config', t.test_env['test_dir'])


if __name__ == "__main__":
    unittest.main()
