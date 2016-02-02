from intmaniac.output.teamcity import TeamcityOutput
from intmaniac.output.base import GenericOutput

import unittest

mock_available = False
try:
    # python 3.something
    from unittest.mock import patch
    from unittest.mock import call
    mock_available = True
except ImportError:
    try:
        # python < 3.something with mock installed
        from mock import patch, call
        mock_available = True
    except ImportError:
        pass
# did I mention this sucks?


class TestWTF(unittest.TestCase):

    @unittest.skipUnless(mock_available, "No mocking available")
    def test_teamcity_output(self):
        # poor man's output test :)
        op = TeamcityOutput()
        with patch.object(TeamcityOutput, 'dump') as mock:
            op.block_open("block")
            op.test_suite_open("suite")
            op.test_open("test")
            op.test_stderr("whoops")
            op.test_stdout("okay")
            op.test_failed("meh")
            op.test_done()
            op.test_suite_done()
            op.block_done()

    def test_text_output(self):
        # poor man's output test :)
        op = GenericOutput()
        with patch.object(GenericOutput, 'dump') as mock:
            op.block_open("block")
            op.test_suite_open("suite")
            op.test_open("test")
            op.test_stderr("whoops")
            op.test_stdout("okay")
            op.test_failed("meh")
            op.test_done()
            op.test_suite_done()
            op.block_done()

