"""Tests for the CLI functionality."""

import unittest
import sys
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from pyenvbuilder.cli import setup_parser, main

class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path("test_project").resolve()
        if not self.test_dir.exists():
            self.test_dir.mkdir()
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_parser_setup(self):
        """Test that the argument parser is set up correctly."""
        parser = setup_parser()
        self.assertIsNotNone(parser)
        
        # Test create command
        args = parser.parse_args(["create", "test_path", "--env-name", "TestEnv"])
        self.assertEqual(args.command, "create")
        self.assertEqual(args.project_path, "test_path")
        self.assertEqual(args.env_name, "TestEnv")
        
        # Test cleanup command
        args = parser.parse_args(["cleanup", "test_env", "--force"])
        self.assertEqual(args.command, "cleanup")
        self.assertEqual(args.env_path, "test_env")
        self.assertTrue(args.force)
        
        # Test xcode command
        args = parser.parse_args(["xcode", "test_project"])
        self.assertEqual(args.command, "xcode")
        self.assertEqual(args.project_path, "test_project")
    
    @patch("pyenvbuilder.cli.create_env")
    def test_create_command(self, mock_create_env):
        """Test the create command."""
        mock_create_env.return_value = True
        
        with patch.object(sys, "argv", ["pyenvbuilder", "create", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 0)
            mock_create_env.assert_called_once_with(str(self.test_dir), "BuildEnv")
    
    @patch("pyenvbuilder.cli.cleanup_env")
    def test_cleanup_command(self, mock_cleanup):
        """Test the cleanup command."""
        mock_cleanup.return_value = True
        
        with patch.object(sys, "argv", ["pyenvbuilder", "cleanup", str(self.test_dir), "--force"]):
            exit_code = main()
            self.assertEqual(exit_code, 0)
            mock_cleanup.assert_called_once_with(str(self.test_dir), True)
    
    @patch("pyenvbuilder.cli.create_xcode_script")
    def test_xcode_command(self, mock_create_script):
        """Test the xcode command."""
        mock_create_script.return_value = True
        
        with patch.object(sys, "argv", ["pyenvbuilder", "xcode", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 0)
            mock_create_script.assert_called_once_with(str(self.test_dir))
    
    def test_no_command(self):
        """Test behavior when no command is provided."""
        with patch.object(sys, "argv", ["pyenvbuilder"]):
            exit_code = main()
            self.assertEqual(exit_code, 1)
    
    @patch("pyenvbuilder.cli.create_env")
    def test_create_command_failure(self, mock_create_env):
        """Test the create command when it fails."""
        mock_create_env.return_value = False
        
        with patch.object(sys, "argv", ["pyenvbuilder", "create", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 1)
    
    @patch("pyenvbuilder.cli.cleanup_env")
    def test_cleanup_command_failure(self, mock_cleanup):
        """Test the cleanup command when it fails."""
        mock_cleanup.return_value = False
        
        with patch.object(sys, "argv", ["pyenvbuilder", "cleanup", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 1)
    
    @patch("pyenvbuilder.cli.create_xcode_script")
    def test_xcode_command_failure(self, mock_create_script):
        """Test the xcode command when it fails."""
        mock_create_script.return_value = False
        
        with patch.object(sys, "argv", ["pyenvbuilder", "xcode", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 1)
    
    @patch("pyenvbuilder.cli.create_env")
    def test_error_handling(self, mock_create_env):
        """Test error handling in the main function."""
        mock_create_env.side_effect=Exception("Test error")
        with patch.object(sys, "argv", ["pyenvbuilder", "create", str(self.test_dir)]):
            exit_code = main()
            self.assertEqual(exit_code, 1)

if __name__ == "__main__":
    unittest.main() 