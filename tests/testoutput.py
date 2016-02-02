from intmaniac import output
from intmaniac.output.teamcity import TeamcityOutput

import unittest


class TestOutput(unittest.TestCase):

    def test_init_output_exception(self):
        with self.assertRaises(ImportError):
            output.init_output("blah")

    def test_init_output(self):
        output.init_output("teamcity")
        self.assertIsInstance(output.output, TeamcityOutput)
