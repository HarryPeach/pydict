import unittest
import importlib.resources
from unittest.mock import patch
from expects import *

import pydict
from pydict.word import Word
import test.resources as x

class Test(unittest.TestCase):
    @patch("pydict.requests.get")
    def test_testable(self, get_mock):
        get_mock.return_value.status_code = 200
        expect(pydict.testable()).to(equal(200))

class TestWord(unittest.TestCase):
    """Tests the word class"""

    def test_word_from_json(self):
        """Tests the constructor of the Word class functions correctly"""
        sample_json = importlib.resources.read_text(x, "sample_ace_response.json")
        example_word = Word(sample_json)

        expect(example_word.word).to(equal("ace"))
        # expect(example_word.definition).to(equal("a playing card with a single spot on it, ranked as the highest card in its suit in most card games"))

if __name__ == "__main__":
    unittest.main()