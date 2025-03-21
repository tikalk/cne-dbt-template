import os
import unittest
from unittest import mock

import pytest

from cli.utils.file_helper import (
    get_models_dir,
    get_resources_dir,
    get_root_dir,
    get_target_dir,
    get_templates_dir,
)

# Assuming get_root_dir is defined in a module named 'module_name'


class TestDirectoryPaths(unittest.TestCase):

    def test_get_root_dir_success(self):
        with mock.patch("os.path.exists", return_value=True), mock.patch("os.getcwd", return_value="/mocked/path"):
            assert get_root_dir() == "/mocked/path"

    def test_get_root_dir_failure(self):
        with mock.patch("os.path.exists", return_value=False):
            with pytest.raises(Exception, match="Running from an unknown directory"):
                get_root_dir()

    @mock.patch("cli.utils.file_helper.get_root_dir")
    def test_get_target_dir(self, mock_get_root_dir):
        # Arrange
        mock_get_root_dir.return_value = "/fake/root"
        expected_path = os.path.join("/fake/root", "target")

        # Act
        result = get_target_dir()

        # Assert
        self.assertEqual(result, expected_path)
        mock_get_root_dir.assert_called_once()

    @mock.patch("cli.utils.file_helper.get_root_dir")
    def test_get_models_dir(self, mock_get_root_dir):
        # Arrange
        mock_get_root_dir.return_value = "/fake/root"
        expected_path = os.path.join("/fake/root", "models")

        # Act
        result = get_models_dir()

        # Assert
        self.assertEqual(result, expected_path)
        mock_get_root_dir.assert_called_once()

    @mock.patch("cli.utils.file_helper.get_root_dir")
    def test_get_resources_dir(self, mock_get_root_dir):
        # Arrange
        mock_get_root_dir.return_value = "/fake/root"
        expected_path = os.path.join("/fake/root", "cli", "resources")

        # Act
        result = get_resources_dir()

        # Assert
        self.assertEqual(result, expected_path)
        mock_get_root_dir.assert_called_once()

    @mock.patch("cli.utils.file_helper.get_resources_dir")
    def test_get_templates_dir(self, mock_get_resources_dir):
        # Arrange
        mock_get_resources_dir.return_value = "/fake/root/cli/resources"
        expected_path = os.path.join("/fake/root/cli/resources", "templates")

        # Act
        result = get_templates_dir()

        # Assert
        self.assertEqual(result, expected_path)
        mock_get_resources_dir.assert_called_once()
