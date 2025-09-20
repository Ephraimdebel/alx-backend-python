#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Test GithubOrgClient.org returns expected value"""
        # Setup the mock return value
        mock_get.return_value = {"mocked": True}

        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert get_json was called once with correct URL
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert org() returns the mocked value
        self.assertEqual(result, {"mocked": True})


if __name__ == "__main__":
    unittest.main()
