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

    def setUp(self):
        self.sample_json = importlib.resources.read_text(x, "sample_ace_response.json")
        self.example_word = Word(self.sample_json)

    def test_word_from_json(self):
        """Tests that the word class can successfully get a word from json response"""
        expect(self.example_word.word).to(equal("ace"))

    def test_definition_from_json(self):
        """Tests that the word class can successfully get a definition from json response"""
        expect(self.example_word.definition).to(equal("a playing card with a single spot on it, ranked as the highest card in its suit in most card games"))

    def test_short_definition_from_json(self):
        """Tests that the word class can successfully get a short definition from json response"""
        expect(self.example_word.short_definition).to(equal("playing card with single spot on it, ranked as highest card in its suit in most card games"))

    def test_invalid_json_indices(self):
        """Test that the word initializer will safely fail when there is no matching indices"""
        self.assertRaises(ValueError, Word, "{}")


if __name__ == "__main__":
    unittest.main()