#!/usr/bin/env python

from intmaniac import prepare_environment, get_test_set_groups
from intmaniac import get_and_init_configuration
from intmaniac.testrun import Testrun
from intmaniac.tools import enable_debug

import unittest
import os
import subprocess as sp

# this is python3 testing only.
# so let's make sure this is not executed on python2
# that sucks *so* much.
mock_available = False
try:
    from unittest.mock import patch
    from unittest.mock import call
    mock_available = True
except ImportError:
    pass


class TestSimpleExecution(unittest.TestCase):

    def setUp(self):
        enable_debug()
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
        with patch("intmaniac.testrun.run_command") as mock:
            mock.side_effect = [
                # args, returncode, stdout is the constructor.
                _construct_return_object(0, [], "hi"),
                _construct_return_object(0, [], None),
                _construct_return_object(0, [], None),
            ]
            expected_calls = [
                call(self.base_cmdline+"echo hi".split()),
                call("docker-compose kill".split(" ")),
                call("docker-compose rm -f".split(" ")),
            ]
            result = tsgs[0][0].run()
            # if you step through here with the IDE the results will be
            # fucked. cause the IDE interferes with the mock.
            # just so you remember.
            self.assertEqual(3, len(mock.mock_calls))
            self.assertEqual(expected_calls, mock.mock_calls)
        for test in tsgs[0][0].tests:
            self.assertIsNone(test.exception)
        self.assertTrue(result)

    @unittest.skipUnless(mock_available,
                         "No mocking available in this Python version")
    def test_for_allowed_failure(self):
        prepare_environment("-c testdata/real_simple_config.yaml".split())
        config = get_and_init_configuration()
        tsgs = get_test_set_groups(config)
        tst = tsgs[0][0].tests[0]
        # we inject the allow_failure attribute here.
        tst.test_meta['allow_failure'] = True
        with patch("intmaniac.testrun.run_command") as mock:
            mock.side_effect = [
                _construct_return_object(1, ['oioi'], "error simulation"),
                _construct_return_object(0, [], None),
                _construct_return_object(0, [], None),
            ]
            result = tst.run()
        self.assertTrue(result)
        self.assertEqual(Testrun.CONTROLLED_FAILURE, tst.state)
