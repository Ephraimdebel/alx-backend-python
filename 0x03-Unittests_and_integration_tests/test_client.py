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
        # Setup the mock to return a fake payload
        mock_get.return_value = {"mocked": True}

        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert get_json called once with the expected URL
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        # Assert the return value matches what mock returned
        self.assertEqual(result, {"mocked": True})
