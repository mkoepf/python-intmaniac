#!/usr/bin/env python

from intmaniac import console_entrypoint
from intmaniac.testrun import Testrun
from intmaniac.tools import enable_debug, _construct_return_object

import unittest
import os

# this is python3 testing only.
# so let's make sure this is not executed on python2
# that sucks *so* much.
mock_available = False
try:
    # python 3.something
    from unittest.mock import patch, call, MagicMock
    mock_available = True
except ImportError:
    try:
        # python < 3.something with mock installed
        from mock import patch, call
        mock_available = True
    except ImportError:
        pass
# did I mention this sucks?


class TestMainExecLoop(unittest.TestCase):

    def setUp(self):
        enable_debug()

    @unittest.skipUnless(mock_available, "No mocking available in this Python version")
    def test_main_exec_loop(self):
        testsets = [MagicMock(), MagicMock(), MagicMock()]
        with patch("intmaniac._get_test_sets") as mock:
            mock.return_value = testsets
            console_entrypoint("-c testdata/command_exec_test.yaml -vvvvv".split())
        for test in testsets:
            self.assertTrue(test.run.called)

