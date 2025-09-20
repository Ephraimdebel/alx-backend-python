#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repos"""
        # Arrange - fake payload
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        # Patch _public_repos_url to return a fixed URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake-url.com"

            # Act
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Assert
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_get_json.assert_called_once_with("http://fake-url.com")
            mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
