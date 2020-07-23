import unittest
import importlib.resources
import os
import argparse
from unittest.mock import patch
from expects import be_a, be_above, equal, expect, be, have_properties, contain

import pydict
import pydict.core
from pydict.word import Word
from pydict.network_manager import NetworkManager
import test.resources as x

class TestWord(unittest.TestCase):
    """Tests the word class"""

    def test_word_attributes(self):
        """Tests that the word class can successfully get a word from json response"""
        example_word = Word("word", "definition")
        expect(example_word.word).to(equal("word"))
        expect(example_word.definition).to(equal("definition"))

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
            expect(word).to(have_properties("word", "definition"))

    @patch("pydict.network_manager.requests.get")
    def test_invalid_request_404(self, get_mock):
        """Tests that the program handles when an entry was not found"""
        get_mock.return_value.status_code = 404
        self.assertRaises(ValueError, NetworkManager.make_request, self, "", "", "", "")

    @patch("pydict.network_manager.requests.get")
    def test_invalid_request_414(self, get_mock):
        """Tests that the program handles when a request url is too long"""
        get_mock.return_value.status_code = 414
        self.assertRaises(ValueError, NetworkManager.make_request, self, "", "", "", "")

    @patch("pydict.network_manager.requests.get")
    def test_invalid_request_500(self, get_mock):
        """Tests that the program handles when a generic internal error occurs"""
        get_mock.return_value.status_code = 500
        self.assertRaises(Exception, NetworkManager.make_request, self, "", "", "", "")

    @patch("pydict.network_manager.requests.get")
    def test_valid_request(self, get_mock):
        """Tests that the program handles a successful request correctly"""
        get_mock.return_value.status_code = 200
        get_mock.return_value.text = "example_request"
        
        expect(NetworkManager.make_request(self, "", "", "", "")).to(be("example_request"))

    @patch("pydict.network_manager.requests.get")
    def test_valid_request_endpoint(self, get_mock):
        """Tests that the request goes to a valid endpoint"""
        get_mock.return_value.status_code = 200

        NetworkManager.make_request(self, "API_KEY", "APP_ID", "x", "y")
        expect(get_mock.call_args_list[0][0]).to(contain(str.format(pydict.core.API_URL, word="x")))


class TestMain(unittest.TestCase):
    """Tests the main class"""

    @patch.dict(os.environ, {pydict.core.API_KEY_STRING: "example_set_string"})
    def test_api_string_provided_through_env(self):
        """Tests that the method will succeed if the key is provided through environment variables"""
        expect(pydict.core.is_api_key_provided([])).to(be(True))

    @patch.dict(os.environ, {pydict.core.APP_ID_STRING: "example_set_string"})
    def test_app_id_string_provided_through_env(self):
        """Tests that the method will succeed if the key is provided through environment variables"""
        expect(pydict.core.is_app_id_provided([])).to(be(True))

    def test_api_string_none_provided(self):
        """Tests that the method will fail when the api is not provided in any valid form"""

        # Set up parser and arguments
        parser = argparse.ArgumentParser(description="test parser")
        parser.add_argument("--api-key")
        args = parser.parse_args()

        # Scrub the environment variable
        os.environ[pydict.core.API_KEY_STRING] = ""
        del os.environ[pydict.core.API_KEY_STRING]

        expect(pydict.core.is_api_key_provided(args)).to(be(False))

    def test_app_id_string_none_provided(self):
        """Tests that the method will fail when the api is not provided in any valid form"""

        # Set up parser and arguments
        parser = argparse.ArgumentParser(description="test parser")
        parser.add_argument("--app-id")
        args = parser.parse_args()

        # Scrub the environment variable
        os.environ[pydict.core.APP_ID_STRING] = ""
        del os.environ[pydict.core.APP_ID_STRING]

        expect(pydict.core.is_app_id_provided(args)).to(be(False))

    def test_api_string_provided_through_args(self):
        """Tests that the method will succeed if the key is passed through arguments"""
        # Set up parser and arguments
        parser = argparse.ArgumentParser(description="test parser")
        parser.add_argument("--api-key")
        args = parser.parse_args(["--api-key", "example_set_string"])

        expect(pydict.core.is_api_key_provided(args)).to(be(True))

    def test_app_id_string_provided_through_args(self):
        """Tests that the method will succeed if the key is passed through arguments"""
        # Set up parser and arguments
        parser = argparse.ArgumentParser(description="test parser")
        parser.add_argument("--app-id")
        args = parser.parse_args(["--app-id", "example_set_string"])

        expect(pydict.core.is_app_id_provided(args)).to(be(True))

if __name__ == "__main__":
    unittest.main(verbosity=2)