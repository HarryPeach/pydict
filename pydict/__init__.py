import argparse
import requests

parser = argparse.ArgumentParser(description="Simple dictionary lookup")

def testable():
    x = requests.get("")
    return x.status_code
