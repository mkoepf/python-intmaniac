#!/usr/bin/env python

from intmaniac.testset import Testset

import unittest


class TTestset(unittest.TestCase):

    def test_global_environment_propagation(self):
        t = Testset()
        t.set_global_config({'environment': {"ho": "wo"}})
        t.add_from_config("added", {})
        self.assertEqual(1, len(t.tests))
        self.assertEqual('wo', t.tests[0].test_env['ho'])


if __name__ == "__main__":
    unittest.main()
