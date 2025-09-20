#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Test that org() returns the correct JSON and calls get_json once"""
        mock_get.return_value = {"mocked": True}
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"mocked": True})

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos")
    ])
    def test_public_repos_url(self, org_name, expected_url):
        """Test that public_repos_url property returns the correct URL"""
        client = GithubOrgClient(org_name)
        # Access the property, not calling it
        self.assertEqual(client._public_repos_url, expected_url)


if __name__ == "__main__":
    unittest.main()
