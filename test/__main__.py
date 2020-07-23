import unittest
import importlib.resources
from unittest.mock import patch
from expects import *

import pydict
from pydict.word import Word
from pydict.network_manager import NetworkManager
import test.resources as x

class Test(unittest.TestCase):
    @patch("pydict.requests.get")
    def test_testable(self, get_mock):
        get_mock.return_value.status_code = 200
        expect(pydict.testable()).to(equal(200))

class TestWord(unittest.TestCase):
    """Tests the word class"""

    def test_word_attributes(self):
        """Tests that the word class can successfully get a word from json response"""
        example_word = Word("word", "definition", "shortDefinition")
        expect(example_word.word).to(equal("word"))
        expect(example_word.definition).to(equal("definition"))
        expect(example_word.shortDefinition).to(equal("shortDefinition"))

class TestNetworkManager(unittest.TestCase):
    """Tests the NetworkManager class"""

    def setUp(self):
        self.sample_json = importlib.resources.read_text(x, "sample_ace_response.json")

    def test_invalid_json_indices(self):
        """Test that the word initializer will safely fail when there is no matching indices"""
        self.assertRaises(ValueError, NetworkManager.words_from_json, self, "{}")

    def test_malformed_json(self):
        """Test that the word initializer will safely fail when the JSON is malformed"""
        self.assertRaises(ValueError, NetworkManager.words_from_json, self, "[}")

    


if __name__ == "__main__":
    unittest.main(verbosity=2)