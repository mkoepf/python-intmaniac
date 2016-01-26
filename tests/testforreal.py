#!/usr/bin/env python

from intmaniac import prepare_environment, get_test_set_groups
from intmaniac import get_and_init_configuration

import unittest
import os
import subprocess as sp

# this is python3 testing only.
# so let's make sure this is not executed on python2
# that sucks *so* much.
mock_available = False
try:
    from unittest.mock import patch
    mock_available = True
except ImportError:
    patch = None


class TestSimpleExecution(unittest.TestCase):

    def setUp(self):
        self.save_dir = os.getcwd()
        base_dir = os.path.realpath("ignoreme/real-test1")
        self.base_cmdline = [
            'docker-compose', 'run', '-e',
            "test_dir=%s" % base_dir,
            '--rm', 'test-service']

    def tearDown(self):
        os.chdir(self.save_dir)

    @unittest.skipUnless(mock_available, "No mocking available in this Python version")
    def test_single_container_setup(self):
        prepare_environment("-c testdata/real_simple_config.yaml".split())
        config = get_and_init_configuration()
        tsgs = get_test_set_groups(config)
        with patch("intmaniac.testrun.sp.run") as mock:
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
