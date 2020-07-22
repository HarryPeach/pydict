import unittest
from unittest.mock import patch
from expects import *
import pydict

class Test(unittest.TestCase):
    @patch("pydict.requests.get")
    def test_testable(self, get_mock):
        get_mock.return_value.status_code = 200

        expect(pydict.testable()).to(equal(200))

if __name__ == "__main__":
    unittest.main()