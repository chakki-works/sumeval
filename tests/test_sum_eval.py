import os
import sys
import unittest
from sumeval.cli.sum_eval import main


class TestSumEval(unittest.TestCase):

    def test_sum_eval(self):
        result = main(
                "r-nlb",
                False,
                False,
                False,
                -1,
                -1,
                "f1",
                0.5,
                "en",
                "I'm living New York its my home town so awesome",
                "My home town is awesome",
            )
