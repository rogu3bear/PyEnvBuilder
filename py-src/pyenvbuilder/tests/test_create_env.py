"""Tests for environment creation functionality."""

import unittest
import sys
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from pyenvbuilder.create_env import create_env, get_env_python

class TestCreateEnv(unittest.TestCase):
    """Test cases for environment creation."""
    
    def setUp(self):
        """Set up test environment."""
        # Use resolve() to get an absolute path for consistent comparisons
        self.test_dir = Path("test_project").resolve()
        self.env_name = "BuildEnv"
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    @patch("subprocess.run")
    def test_create_env_success(self, mock_run):
        """Test successful environment creation."""
        mock_run.return_value = MagicMock(returncode=0)
        
        success = create_env(str(self.test_dir), self.env_name)
        self.assertTrue(success)
        
        # Verify subprocess calls
        calls = mock_run.call_args_list
        self.assertEqual(len(calls), 3)  # venv creation, pip upgrade, requirements install
        
        # Check venv creation call
        # Compare resolved paths
        expected_path = str(self.test_dir / self.env_name)
        actual_path = str(calls[0][0][0][3]) 
        self.assertEqual(actual_path, expected_path)
        
        # Check pip upgrade call
        # Compare resolved paths for python executable
        expected_python_path = get_env_python(str(self.test_dir), self.env_name)
        if expected_python_path: # Should exist after successful mock creation
            self.assertEqual(calls[1][0][0], [str(expected_python_path), "-m", "pip", "install", "--upgrade", "pip"])
        
            # Check requirements install call
            self.assertEqual(calls[2][0][0][:5], [str(expected_python_path), "-m", "pip", "install"])
            self.assertTrue(all(req in calls[2][0][0] for req in ["wheel", "setuptools", "pip-tools"]))
    
    def test_create_env_existing(self):
        """Test environment creation when it already exists."""
        env_path = self.test_dir / self.env_name
        env_path.mkdir()
        
        success = create_env(str(self.test_dir), self.env_name)
        self.assertFalse(success)
    
    def test_create_env_invalid_project(self):
        """Test environment creation with invalid project path."""
        success = create_env("nonexistent", self.env_name)
        self.assertFalse(success)
    
    @patch("subprocess.run")
    def test_create_env_pip_failure(self, mock_run):
        """Test environment creation when pip upgrade fails."""
        mock_run.side_effect = [
            MagicMock(returncode=0),  # venv creation succeeds
            subprocess.CalledProcessError(1, "cmd") # pip upgrade fails
        ]
        
        success = create_env(str(self.test_dir), self.env_name)
        self.assertFalse(success)
    
    @patch("subprocess.run")
    def test_create_env_requirements_failure(self, mock_run):
        """Test environment creation when requirements installation fails."""
        mock_run.side_effect = [
            MagicMock(returncode=0),  # venv creation succeeds
            MagicMock(returncode=0),  # pip upgrade succeeds
            subprocess.CalledProcessError(1, "cmd") # requirements install fails
        ]
        
        success = create_env(str(self.test_dir), self.env_name)
        self.assertFalse(success)
    
    def test_get_env_python_success(self):
        """Test getting Python executable path."""
        env_path = self.test_dir / self.env_name
        env_path.mkdir()
        if sys.platform == "win32":
            python_path = env_path / "Scripts" / "python.exe"
        else:
            python_path = env_path / "bin" / "python"
        python_path.parent.mkdir(parents=True)
        python_path.touch()
        
        result = get_env_python(str(self.test_dir), self.env_name)
        # Compare resolved paths
        self.assertEqual(str(result), str(python_path.resolve()))
    
    def test_get_env_python_nonexistent(self):
        """Test getting Python executable path when environment doesn't exist."""
        result = get_env_python(str(self.test_dir), self.env_name)
        self.assertIsNone(result)
    
    def test_get_env_python_no_python(self):
        """Test getting Python executable path when Python executable doesn't exist."""
        env_path = self.test_dir / self.env_name
        env_path.mkdir()
        
        result = get_env_python(str(self.test_dir), self.env_name)
        self.assertIsNone(result)
    
    def test_get_env_python_invalid_project(self):
        """Test getting Python executable path with invalid project path."""
        result = get_env_python("nonexistent", self.env_name)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main() 