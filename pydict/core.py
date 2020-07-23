import argparse
import requests
import os

from pydict.network_manager import NetworkManager

API_KEY_STRING = "PYDICT_API_KEY"

def main():
    parser = argparse.ArgumentParser(description="Simple dictionary lookup using Oxford Dictionaries API")
    parser.add_argument("query", type=str, help="the search query")
    parser.add_argument("--api-key", type=str, help="the API key to access the dictionaries API")

    ARGS = parser.parse_args()
    NETWORK_MANAGER = NetworkManager()
    
    # Check if the API key has been provided
    if not is_api_key_provided(ARGS):
        print("You haven't provided an API key, please see the README for more info.")
        exit()

    json = ""
    try:
        json = NETWORK_MANAGER.make_request("", "", "")
    except Exception as e:
        print(e)
        exit(1)

def is_api_key_provided(args):
    """Checks if the API key is provided in any valid form

    Args:
        args (argparse.Namespace): The arguments provided to the program
    """
    if (os.getenv(API_KEY_STRING) == None) and (args.api_key == None):
        return False
    return True


