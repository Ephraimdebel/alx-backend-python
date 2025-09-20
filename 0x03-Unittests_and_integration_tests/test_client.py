#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import sys
import os
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected value from org"""
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and calls dependencies"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        test_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos returns only repos with given license"""
        test_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
            {"name": "repo4", "license": None},
        ]
        mock_get_json.return_value = test_payload
        test_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("testorg")
            result = client.public_repos(license="apache-2.0")
            self.assertEqual(result, ["repo1", "repo3"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

        @parameterized.expand([
                ({"license": {"key": "my_license"}}, "my_license", True),
                ({"license": {"key": "other_license"}}, "my_license", False),
            ])
        def test_has_license(self, repo, license_key, expected):
            """Unit-test GithubOrgClient.has_license with parameterized inputs"""
            client = GithubOrgClient("testorg")
            self.assertEqual(client.has_license(repo, license_key), expected)

    def test_repos_payload_memoization(self):
        """Test repos_payload is memoized and get_json called once"""
        with patch('client.get_json', return_value=[{"name": "repo"}]) as mock_get_json, \
             patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "url"
            client = GithubOrgClient("testorg")
            # Call twice, should only call get_json once due to memoization
            client.repos_payload
            client.repos_payload
            mock_get_json.assert_called_once_with("url")

    def test_org_memoization(self):
        """Test org property is memoized and get_json called once"""
        test_payload = {"login": "testorg"}
        with patch('client.get_json', return_value=test_payload) as mock_get_json:
            client = GithubOrgClient("testorg")
            result1 = client.org
            result2 = client.org
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg")
            self.assertEqual(result1, test_payload)
            self.assertEqual(result2, test_payload)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = unittest.mock.Mock()
            mock_response.status_code = 200
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos without license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()