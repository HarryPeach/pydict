import json
import requests
from pydict.word import Word

class NetworkManager:
    def make_request(self, api_key, word, options):
        """Makes a request and returns the json response

        Args:
            api_key (string): The Oxford Dictionaries API key
            word (string): The word to search for
            options (TODO): The options for the search
        """
        res = requests.get("https://od-api.oxforddictionaries.com:443/api/v2/entries/")

        if res.status_code == 200:
            pass
        elif res.status_code == 404:
            raise ValueError("There was no word found matching the given criteria.")


    def words_from_json(self, json_input):
        """Decodes the json response into a list of Words

        Args:
            json_input (string): The json to be decoded

        Raises:
            ValueError: If specific required indices were not found
            ValueError: If the json provided is malformed

        Returns:
            words[]: A list of words from the json response
        """
        json_parsed = json.loads(json_input)
        words = []

        try:
            for result in json_parsed["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]:
                words.append(Word(json_parsed["id"], result["definitions"][0], result["shortDefinitions"][0]))

            return words
        except KeyError:
            raise ValueError("The JSON did not contain the required indices.")
        except json.decoder.JSONDecodeError:
            raise ValueError("The JSON passed to the class was malformed.")
