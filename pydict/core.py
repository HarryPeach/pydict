import argparse
import requests
import os
import sys

from pydict.network_manager import NetworkManager

API_KEY_STRING = "PYDICT_API_KEY"
APP_ID_STRING = "PYDICT_APP_ID"
API_URL = "https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb/{word}?fields=definitions,pronunciations"

def main():
    unix_mode = False
    unix_args = ""

    parser = argparse.ArgumentParser(description="Simple dictionary lookup using Oxford Dictionaries API")
    parser.add_argument("-x", "--unix", type=bool, nargs="?", const=True, default=False, help="'Unix mode', enables piped input")
    parser.add_argument("query", nargs="?", type=str, help="the search query")
    parser.add_argument("--app-id", type=str, help="the app ID to access the dictionaries API")
    parser.add_argument("--api-key", type=str, help="the API key to access the dictionaries API")
    parser.add_argument("-a", "--all", type=bool, nargs="?", const=True, default=False, help="prints all available information")

    ARGS = parser.parse_args()
    NETWORK_MANAGER = NetworkManager()
    
    # Check if the API key has been provided
    if not is_api_key_provided(ARGS):
        print("You haven't provided an API key, please see the README for more info.")
        exit(1)

    # Check that an app ID has been provided
    if not is_app_id_provided(ARGS):
        print("You haven't provided an app ID, please see the README for more info.")
        exit(1)

    # Set the API_KEY from given source
    API_KEY = ""
    if ARGS.api_key != None:
        API_KEY = ARGS.api_key
    else:
        API_KEY = os.getenv(API_KEY_STRING)

    # Set the APP_ID from given source
    APP_ID = ""
    if ARGS.app_id != None:
        APP_ID = ARGS.app_id
    else:
        APP_ID = os.getenv(APP_ID_STRING)

    # Enable unix mode if specified
    if ARGS.unix == True:
        unix_mode = True
        unix_args = sys.stdin.read().rstrip()
    else:
        if ARGS.query is None:
            parser.error("A query is required if the program is not run in UNIX mode")

    json = ""
    try:
        if unix_mode: 
            json = NETWORK_MANAGER.make_request(API_KEY, APP_ID, unix_args, "")
        else:
            json = NETWORK_MANAGER.make_request(API_KEY, APP_ID, ARGS.query, "")
        words = NETWORK_MANAGER.words_from_json(json)
        print_definition(words[0], ARGS)

    except Exception as e:
        print(e)
        exit(1)

def print_definition(word, args):
    """Prints the definition in a formatted way"""
    if args.all:
        print(f"{word.word} • /{word.pronunciation}/")
        print(word.definition)
    else:
        print(word.definition)

def is_api_key_provided(args):
    """Checks if the API key is provided in any valid form

    Args:
        args (argparse.Namespace): The arguments provided to the program
    """
    if (os.getenv(API_KEY_STRING) == None) and (args.api_key == None):
        return False
    return True

def is_app_id_provided(args):
    """Checks if the APP id is provided in any valid form

    Args:
        args (argparse.Namespace): The arguments provided to the program
    """
    if (os.getenv(APP_ID_STRING) == None) and (args.app_id == None):
        return False
    return True


