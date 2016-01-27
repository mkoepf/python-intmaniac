#!/usr/bin/env pythpn

from intmaniac import prepare_environment, get_test_set_groups
from intmaniac import get_and_init_configuration

import unittest
import os
import os.path


class TestTemplateEmpty(unittest.TestCase):

    def setUp(self):
        prepare_environment("-c testdata/testconfig_empty.yaml".split())
        config = get_and_init_configuration()
        self.tsgs = get_test_set_groups(config)

    def testNumberOfTestsetsCreated(self):
        tsgs = self.tsgs
        self.assertIsInstance(tsgs, list)
        self.assertEqual(len(tsgs), 1)
        self.assertIsInstance(tsgs[0], list)
        self.assertEqual(0, len(tsgs[0]))


class TestTemplateArrayTriple(unittest.TestCase):

    def setUp(self):
        prepare_environment("-c testdata/testconfig_array_triple.yaml".split())
        config = get_and_init_configuration()
        self.tsgs = get_test_set_groups(config)

    def test_created_testset_groups(self):
        tsgs = self.tsgs
        self.assertIsInstance(tsgs, list)
        self.assertEqual(len(tsgs), 2)
        self.assertIsInstance(tsgs[0], list)
        self.assertIsInstance(tsgs[1], list)
        self.assertEqual(2, len(tsgs[0]))
        self.assertEqual(1, len(tsgs[1]))

    def test_given_names(self):
        tsgs = self.tsgs
        self.assertEqual(tsgs[0][0].name, "00-ts1")
        self.assertEqual(tsgs[0][1].name, "00-ts2")
        self.assertEqual(tsgs[1][0].name, "01-ts3")

    def test_environment_setting_and_propagation(self):
        tlcount = 0
        tscount = 1
        tcount = 1
        tsgs = self.tsgs
        for tlist in tsgs:
            for tset in tlist:
                tests = sorted(tset.tests, key=lambda x: x.name)
                for test in tests:
                    tname = "%02d-ts%d-test%d" % (tlcount, tscount, tcount)
                    self.assertEqual(tname, test.name)
                    self.assertEqual(test.test_env[str(tcount)], str(tcount))
                    tcount += 1
                tscount += 1
            tlcount += 1


class TestTemplateKeysTriple(unittest.TestCase):

    def setUp(self):
        prepare_environment("-c testdata/testconfig_keys_triple.yaml".split())
        config = get_and_init_configuration()
        self.tsgs = get_test_set_groups(config)

    def test_created_testset_groups(self):
        tsgs = self.tsgs
        self.assertIsInstance(tsgs, list)
        self.assertEqual(len(tsgs), 1)
        self.assertIsInstance(tsgs[0], list)
        self.assertEqual(3, len(tsgs[0]))

    def test_given_names(self):
        tsgs = self.tsgs
        self.assertEqual(tsgs[0][0].name, "ts1")
        self.assertEqual(tsgs[0][1].name, "ts2")
        self.assertEqual(tsgs[0][2].name, "ts3")

    def test_environment_setting_and_propagation(self):
        tscount = 1
        tcount = 1
        tsgs = self.tsgs
        for tlist in tsgs:
            for tset in tlist:
                tests = sorted(tset.tests, key=lambda x: x.name)
                for test in tests:
                    tname = "ts%d-test%d" % (tscount, tcount)
                    self.assertEqual(tname, test.name)
                    self.assertEqual(test.test_env[str(tcount)], str(tcount))
                    tcount += 1
                tscount += 1


class TestTemplateSubglobals(unittest.TestCase):

    def setUp(self):
        self.test_data = "testdata/testconfig_sub_globals.yaml"
        prepare_environment(["-c", self.test_data])
        config = get_and_init_configuration()
        self.tsgs = get_test_set_groups(config)

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
        self.assertEqual(1, len(self.tsgs))
        self.assertEqual(1, len(self.tsgs[0]))
        self.assertEqual(1, len(self.tsgs[0][0].tests))
        tst = self.tsgs[0][0].tests[0]
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
