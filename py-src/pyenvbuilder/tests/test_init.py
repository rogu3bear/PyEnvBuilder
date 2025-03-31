"""Tests for the main package initialization."""

import unittest
import os
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from pyenvbuilder import create_xcode_script, setup_xcode_project

class TestInit(unittest.TestCase):
    """Test cases for package initialization."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path("test_project").resolve()
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_create_xcode_script_success(self):
        """Test successful creation of Xcode script."""
        success = create_xcode_script(str(self.test_dir))
        self.assertTrue(success)
        
        script_path = self.test_dir / "setup_python_env.sh"
        self.assertTrue(script_path.exists())
        self.assertTrue(os.access(script_path, os.X_OK))
        
        # Verify script content
        content = script_path.read_text()
        self.assertIn("#!/bin/bash", content)
        self.assertIn("BuildEnv", content)
        self.assertIn("python3 -m venv", content)
    
    def test_create_xcode_script_nonexistent_dir(self):
        """Test creating script in nonexistent directory."""
        success = create_xcode_script("nonexistent")
        self.assertFalse(success)
    
    def test_create_xcode_script_permission_error(self):
        """Test creating script when permission denied."""
        # Create a file instead of a directory
        test_file = self.test_dir / "test.txt"
        test_file.touch()
        
        with patch("os.chmod") as mock_chmod:
            mock_chmod.side_effect = PermissionError()
            success = create_xcode_script(str(self.test_dir))
            self.assertFalse(success)
    
    @patch("pyenvbuilder.run_all_checks")
    @patch("pyenvbuilder.create_env")
    @patch("pyenvbuilder.create_xcode_script")
    def test_setup_xcode_project_success(self, mock_create_script, mock_create_env, mock_run_checks):
        """Test successful setup of Xcode project."""
        # Mock successful checks
        mock_run_checks.return_value = (True, ["✓ Check 1", "✓ Check 2"])
        mock_create_env.return_value = True
        mock_create_script.return_value = True
        
        success = setup_xcode_project(str(self.test_dir))
        self.assertTrue(success)
        
        # Verify all mocks were called
        mock_run_checks.assert_called_once_with(str(self.test_dir))
        mock_create_env.assert_called_once_with(str(self.test_dir))
        mock_create_script.assert_called_once_with(str(self.test_dir))
    
    @patch("pyenvbuilder.run_all_checks")
    def test_setup_xcode_project_check_failure(self, mock_run_checks):
        """Test setup when pre-installation checks fail."""
        mock_run_checks.return_value = (False, ["✗ Check failed"])
        
        success = setup_xcode_project(str(self.test_dir))
        self.assertFalse(success)
    
    @patch("pyenvbuilder.run_all_checks")
    @patch("pyenvbuilder.create_env")
    def test_setup_xcode_project_env_failure(self, mock_create_env, mock_run_checks):
        """Test setup when environment creation fails."""
        mock_run_checks.return_value = (True, ["✓ Check 1"])
        mock_create_env.return_value = False
        
        success = setup_xcode_project(str(self.test_dir))
        self.assertFalse(success)
    
    @patch("pyenvbuilder.run_all_checks")
    @patch("pyenvbuilder.create_env")
    @patch("pyenvbuilder.create_xcode_script")
    def test_setup_xcode_project_script_failure(self, mock_create_script, mock_create_env, mock_run_checks):
        """Test setup when script creation fails."""
        mock_run_checks.return_value = (True, ["✓ Check 1"])
        mock_create_env.return_value = True
        mock_create_script.return_value = False
        
        success = setup_xcode_project(str(self.test_dir))
        self.assertFalse(success)
    
    def test_setup_xcode_project_nonexistent_dir(self):
        """Test setup with nonexistent directory."""
        success = setup_xcode_project("nonexistent")
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main() 