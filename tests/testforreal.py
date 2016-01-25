#!/usr/bin/env python

from testrunner import prepare_environment, get_test_set_groups
from testrunner import get_and_init_configuration

import unittest
from unittest.mock import patch
import os

# for the tests
import subprocess as sp


class TestSimpleExecution(unittest.TestCase):

    def setUp(self):
        self.save_dir = os.getcwd()
        base_dir = os.path.realpath("../ignoreme/real-test1")
        self.base_cmdline = [
            'docker-compose', 'run', '-e',
            "test_dir=%s" % base_dir,
            '--rm', 'test-service']

    def tearDown(self):
        os.chdir(self.save_dir)

    def test_single_container_setup(self):
        prepare_environment("-c ../testdata/real_simple_config.yaml".split())
        config = get_and_init_configuration()
        tsgs = get_test_set_groups(config)
        with patch("runner.testrun.sp.run") as mock:
            mock.return_value = sp.CompletedProcess(args=[], returncode=0, stdout="hi")
            result = tsgs[0][0].run()
            mock.assert_called_with(self.base_cmdline+"echo hi".split(),
                                    check=True,
                                    stdout=sp.PIPE, stderr=sp.STDOUT,
                                    universal_newlines=True)
        tsgs[0][0].dump()
        for test in tsgs[0][0].tests:
            self.assertIsNone(test.exception)
        self.assertTrue(result)
