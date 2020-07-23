import json
from pydict.word import Word

class NetworkManager:
    def words_from_json(self, json_input):
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
