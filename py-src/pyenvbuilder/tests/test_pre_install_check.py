"""Tests for pre-installation checks."""

import unittest
import sys
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from pyenvbuilder.pre_install_check import (
    check_python_version,
    check_venv_available,
    check_pip_available,
    check_xcode_command_line_tools,
    check_project_directory,
    run_all_checks
)

class TestPreInstallCheck(unittest.TestCase):
    """Test cases for pre-installation checks."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path("test_project")
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_check_python_version(self):
        """Test Python version check."""
        success, message = check_python_version()
        self.assertTrue(success)
        self.assertTrue(message.startswith("✓"))
        
        # Test with older version
        with patch("sys.version_info", (3, 5)):
            success, message = check_python_version()
            self.assertFalse(success)
            self.assertFalse(message.startswith("✓"))
    
    def test_check_venv_available(self):
        """Test venv availability check."""
        success, message = check_venv_available()
        self.assertTrue(success)
        self.assertTrue(message.startswith("✓"))
        
        # Test when venv is not available
        with patch.dict(sys.modules, {"venv": None}):
            success, message = check_venv_available()
            self.assertFalse(success)
            self.assertFalse(message.startswith("✓"))
    
    def test_check_pip_available(self):
        """Test pip availability check."""
        with patch("subprocess.run") as mock_run:
            # Simulate success
            mock_run.return_value = MagicMock(returncode=0)
            success, message = check_pip_available()
            self.assertTrue(success)
            self.assertTrue(message.startswith("✓"))
            mock_run.assert_called_once()

            # Simulate failure
            mock_run.reset_mock()
            mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
            success, message = check_pip_available()
            self.assertFalse(success)
            self.assertFalse(message.startswith("✓"))
            mock_run.assert_called_once()
    
    def test_check_xcode_command_line_tools(self):
        """Test Xcode Command Line Tools check."""
        with patch("subprocess.run") as mock_run:
            # Simulate success
            mock_run.return_value = MagicMock(returncode=0)
            success, message = check_xcode_command_line_tools()
            self.assertTrue(success)
            self.assertTrue(message.startswith("✓"))
            mock_run.assert_called_once()

            # Simulate failure
            mock_run.reset_mock()
            mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
            success, message = check_xcode_command_line_tools()
            self.assertFalse(success)
            self.assertFalse(message.startswith("✓"))
            mock_run.assert_called_once()
    
    def test_check_project_directory(self):
        """Test project directory check."""
        success, message = check_project_directory(str(self.test_dir))
        self.assertTrue(success)
        self.assertTrue(message.startswith("✓"))
        
        success, message = check_project_directory("nonexistent")
        self.assertFalse(success)
        self.assertFalse(message.startswith("✓"))
        
        # Create a file instead of a directory
        test_file = self.test_dir / "test.txt"
        test_file.touch()
        success, message = check_project_directory(str(test_file))
        self.assertFalse(success)
        self.assertFalse(message.startswith("✓"))
    
    def test_run_all_checks(self):
        """Test running all checks."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            success, messages = run_all_checks(str(self.test_dir))
            self.assertTrue(success)
            self.assertEqual(len(messages), 5)  # All checks should run
            self.assertTrue(all(msg.startswith("✓") for msg in messages))
            
            # Test with failing checks
            with patch("sys.version_info", (3, 5)):
                success, messages = run_all_checks(str(self.test_dir))
                self.assertFalse(success)
                self.assertFalse(all(msg.startswith("✓") for msg in messages))
    
    def test_run_all_checks_invalid_project(self):
        """Test running all checks with invalid project path."""
        success, messages = run_all_checks("nonexistent")
        self.assertFalse(success)
        self.assertFalse(all(msg.startswith("✓") for msg in messages))

if __name__ == "__main__":
    unittest.main() 