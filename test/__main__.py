import unittest
import importlib.resources
from unittest.mock import patch
from expects import *

import pydict
from pydict.word import Word
from pydict.network_manager import NetworkManager
import test.resources as x

class TestWord(unittest.TestCase):
    """Tests the word class"""

    def test_word_attributes(self):
        """Tests that the word class can successfully get a word from json response"""
        example_word = Word("word", "definition", "shortDefinition")
        expect(example_word.word).to(equal("word"))
        expect(example_word.definition).to(equal("definition"))
        expect(example_word.short_definition).to(equal("shortDefinition"))

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

    def test_word_list(self):
        """Tests that the json decoder returns a list of words"""
        words = NetworkManager.words_from_json(self, self.sample_json)

        expect(len(words)).to(be_above(0))
        for word in words:
            expect(word).to(be_a(Word))

    def test_word_list_validity(self):
        """Tests the the words returned from the json decoder are valid"""
        words = NetworkManager.words_from_json(self, self.sample_json)

        for word in words:
            expect(word).to(have_properties("word", "definition", "short_definition"))

    @patch("pydict.requests.get")
    def test_invalid_request_404(self, get_mock):
        """Tests that the program handles when an entry was not found"""
        get_mock.return_value.status_code = 404
        self.assertRaises(ValueError, NetworkManager.make_request, self, "", "", "")

    


if __name__ == "__main__":
    unittest.main(verbosity=2)