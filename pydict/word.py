import json

class Word:
    def __init__(self, json_input):
        json_parsed = json.loads(json_input)
        try:
            self.word = json_parsed["id"]
            self.definition = json_parsed["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            self.short_definition = json_parsed["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["shortDefinitions"][0]
        except KeyError:
            raise ValueError("The JSON passed to the class was malformed.")

        