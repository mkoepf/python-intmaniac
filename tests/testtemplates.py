#!/usr/bin/env pythpn

from intmaniac import _prepare_environment, _get_test_sets
from intmaniac import _get_and_init_configuration
from intmaniac.testset import Testset
from intmaniac.testrun import Testrun
from intmaniac.tools import enable_debug

import unittest


class TestTemplateEmpty(unittest.TestCase):

    def setUp(self):
        enable_debug()
        _prepare_environment("-c testdata/testconfig_empty.yaml".split())
        config = _get_and_init_configuration()
        self.testsets = _get_test_sets(config)

    def testNumberOfTestsetsCreated(self):
        testsets = self.testsets
        self.assertIsInstance(testsets, list)
        self.assertEqual(len(testsets), 0)


class TestTemplateKeysTriple(unittest.TestCase):

    def setUp(self):
        enable_debug()
        _prepare_environment("-c testdata/testconfig_keys_triple.yaml".split())
        config = _get_and_init_configuration()
        self.testsets = _get_test_sets(config)

    def test_created_testset_groups(self):
        testsets = self.testsets
        self.assertIsInstance(testsets, list)
        self.assertEqual(len(testsets), 3)
        for testset in testsets:
            self.assertIsInstance(testset, Testset)

    def test_given_names(self):
        testsets = self.testsets
        self.assertEqual(testsets[0].name, "ts1")
        self.assertEqual(testsets[1].name, "ts2")
        self.assertEqual(testsets[2].name, "ts3")

    def test_environment_setting_and_propagation(self):
        tscount = 1
        tcount = 1
        testsets = self.testsets
        for tset in testsets:
            tests = sorted(tset.tests, key=lambda x: x.name)
            for test in tests:
                tname = "ts%d-test%d" % (tscount, tcount)
                self.assertEqual(tname, test.name)
                self.assertEqual(test.test_env[str(tcount)], str(tcount))
                tcount += 1
            tscount += 1


class TestTemplateSubglobals(unittest.TestCase):

    def setUp(self):
        enable_debug()
        self.test_data = "testdata/testconfig_sub_globals.yaml"
        _prepare_environment(["-c", self.test_data])
        config = _get_and_init_configuration()
        self.testsets = _get_test_sets(config)

    def test_subglobal_propagation(self):
        meta_dict = [
            ('heey', 'oooh'),
            ('whoops', 'ydoopsy'),
            ('and', 'quickly'),
            ('anastasia', 'mr grey'),
            ('oh', 'just do it already'),
        ]
        env_dict = [
            ('this_is', 'in all'),
            ('this_should', 'be cool'),
            ('and_this', 'is there, too'),
            ('while_this', 'but this'),
            ('and', 'one for me, too'),
        ]
        self.assertEqual(1, len(self.testsets))
        self.assertEqual(1, len(self.testsets[0].tests))
        tst = self.testsets[0].tests[0]
        for pair in ((tst.test_env, env_dict), (tst.test_meta, meta_dict)):
            tested, tester = pair
            for key, val in tester:
                self.assertTrue(key in tested,
                                "key '%s' is not in %s" % (key, tested))
                self.assertEqual(val, tested[key],
                                 "value of tested['%s'] does not match '%s'"
                                 % (key, val))

if __name__ == "__main__":
    unittest.main()
