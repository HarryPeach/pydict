import json

class Word:
    def __init__(self, json_input):
        json_parsed = json.loads(json_input)
        # self.definiton = json_parsed["definitions"]
        self.word = ""
        self.definition = ""