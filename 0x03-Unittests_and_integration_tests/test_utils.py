#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map function
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest import TestCase
from unittest.mock import patch
from utils import get_json

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError with correct message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

class TestGetJson(TestCase):
    """Unit tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected result with mocked requests.get"""

        # Configure mock: mock_get() -> mock_response -> .json() -> test_payload
        mock_get.return_value.json.return_value = test_payload

        # Call the function under test
        result = get_json(test_url)

        # Verify requests.get was called once with the test_url
        mock_get.assert_called_once_with(test_url)

        # Verify the function returned the correct payload
        self.assertEqual(result, test_payload)
if __name__ == "__main__":
    unittest.main()
