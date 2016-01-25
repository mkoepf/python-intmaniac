#!/usr/bin/env python

from testrunner import prepare_environment, get_test_set_groups
from testrunner import get_and_init_configuration

import unittest
import os


class TestSimpleExecution(unittest.TestCase):

    def setUp(self):
        self.save_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self.save_dir)

    def test_single_container_setup(self):
        prepare_environment("-c ../testdata/real_simple_config.yaml".split())
        config = get_and_init_configuration()
        tsgs = get_test_set_groups(config)
        result = tsgs[0][0].run()
        tsgs[0][0].dump()
        for test in tsgs[0][0].tests:
            self.assertIsNone(test.exception)
        self.assertTrue(result)
