"""Tests for environment cleanup functionality."""

import unittest
import sys
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from pyenvbuilder.cleanup import cleanup_env, is_valid_venv

class TestCleanup(unittest.TestCase):
    """Test cases for environment cleanup."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path("test_project")
        self.test_dir.mkdir(exist_ok=True)
        self.env_name = "BuildEnv"
        self.env_path = self.test_dir / self.env_name
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            for file in self.test_dir.glob("*"):
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
            self.test_dir.rmdir()
    
    def create_test_env(self):
        """Create a test virtual environment."""
        self.env_path.mkdir()
        if sys.platform == "win32":
            python_path = self.env_path / "Scripts" / "python.exe"
        else:
            python_path = self.env_path / "bin" / "python"
        python_path.parent.mkdir(parents=True)
        python_path.touch()
    
    def test_cleanup_env_success(self):
        """Test successful environment cleanup."""
        self.create_test_env()
        
        success = cleanup_env(str(self.env_path), force=True)
        self.assertTrue(success)
        self.assertFalse(self.env_path.exists())
    
    def test_cleanup_env_nonexistent(self):
        """Test cleanup of nonexistent environment."""
        success = cleanup_env(str(self.env_path), force=True)
        self.assertFalse(success)
    
    def test_cleanup_env_invalid(self):
        """Test cleanup of invalid environment."""
        self.env_path.mkdir()
        success = cleanup_env(str(self.env_path), force=True)
        self.assertFalse(success)
    
    @patch("builtins.input")
    def test_cleanup_env_confirmation(self, mock_input):
        """Test cleanup confirmation."""
        self.create_test_env()
        
        # Test confirmation
        mock_input.return_value = "y"
        success = cleanup_env(str(self.env_path), force=False)
        self.assertTrue(success)
        self.assertFalse(self.env_path.exists())
        
        # Test cancellation
        self.create_test_env()
        mock_input.return_value = "n"
        success = cleanup_env(str(self.env_path), force=False)
        self.assertFalse(success)
        self.assertTrue(self.env_path.exists())
    
    def test_cleanup_env_permission_error(self):
        """Test cleanup with permission error."""
        self.create_test_env()
        
        # Make directory read-only
        if sys.platform != "win32":  # Skip on Windows
            self.env_path.chmod(0o444)
            success = cleanup_env(str(self.env_path), force=True)
            self.assertFalse(success)
            self.assertTrue(self.env_path.exists())
            self.env_path.chmod(0o755)  # Restore permissions
    
    def test_is_valid_venv_success(self):
        """Test valid virtual environment check."""
        self.create_test_env()
        self.assertTrue(is_valid_venv(self.env_path))
    
    def test_is_valid_venv_nonexistent(self):
        """Test valid virtual environment check with nonexistent path."""
        self.assertFalse(is_valid_venv(self.env_path))
    
    def test_is_valid_venv_invalid(self):
        """Test valid virtual environment check with invalid path."""
        self.env_path.mkdir()
        self.assertFalse(is_valid_venv(self.env_path))
    
    def test_is_valid_venv_no_python(self):
        """Test valid virtual environment check without Python executable."""
        self.env_path.mkdir()
        if sys.platform == "win32":
            (self.env_path / "Scripts").mkdir()
        else:
            (self.env_path / "bin").mkdir()
        self.assertFalse(is_valid_venv(self.env_path))

if __name__ == "__main__":
    unittest.main() 