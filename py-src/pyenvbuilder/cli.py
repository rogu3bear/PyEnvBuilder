"""Command-line interface for PyEnvBuilder."""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, Tuple

from .create_env import create_env
from .cleanup import cleanup_env
from .pre_install_check import run_all_checks
from .logging_config import setup_logging
from .config import config

# Configure logging
setup_logging()

logger = logging.getLogger(__name__)

def setup_parser() -> argparse.ArgumentParser:
    """Set up the argument parser with all commands and options."""
    parser = argparse.ArgumentParser(
        description="PyEnvBuilder - A tool for managing Python virtual environments in Xcode projects"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new virtual environment")
    create_parser.add_argument(
        "--project-path",
        type=str,
        default=os.getcwd(),
        help="Path to the Xcode project directory"
    )
    create_parser.add_argument(
        "--env-name",
        type=str,
        help="Name of the virtual environment (default: BuildEnv)"
    )
    create_parser.add_argument(
        "--python-version",
        type=str,
        help="Required Python version (default: 3.6)"
    )
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up an existing virtual environment")
    cleanup_parser.add_argument(
        "--project-path",
        type=str,
        default=os.getcwd(),
        help="Path to the Xcode project directory"
    )
    cleanup_parser.add_argument(
        "--force",
        action="store_true",
        help="Force cleanup without confirmation"
    )
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Run pre-installation checks")
    check_parser.add_argument(
        "--project-path",
        type=str,
        default=os.getcwd(),
        help="Path to the Xcode project directory"
    )
    
    # Global options
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output"
    )
    
    return parser

def parse_args() -> argparse.Namespace:
    """Parse command line arguments using the setup parser."""
    parser = setup_parser()
    return parser.parse_args()

def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Update logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # Update configuration with command line arguments
    if hasattr(args, "env_name") and args.env_name:
        config.set("env_name", args.env_name)
    if hasattr(args, "python_version") and args.python_version:
        config.set("python_version", args.python_version)
    
    project_path = Path(args.project_path).resolve()
    
    try:
        if args.command == "create":
            # Run pre-installation checks
            success, messages = run_all_checks(str(project_path))
            for msg in messages:
                if msg.startswith("✓"):
                    logger.info(msg)
                else:
                    logger.error(msg)
            if not success:
                return 1
                
            # Create virtual environment
            success, error_msg = create_env(str(project_path))
            if not success:
                logger.error(error_msg)
                return 1
                
            logger.info("Successfully created Python environment")
            return 0
            
        elif args.command == "cleanup":
            # Clean up environment
            success, error_msg = cleanup_env(str(project_path), force=args.force)
            if not success:
                logger.error(error_msg)
                return 1
                
            logger.info("Successfully cleaned up Python environment")
            return 0
            
        elif args.command == "check":
            # Run checks only
            success, messages = run_all_checks(str(project_path))
            for msg in messages:
                if msg.startswith("✓"):
                    logger.info(msg)
                else:
                    logger.error(msg)
            return 0 if success else 1
            
        else:
            logger.error("No command specified. Use --help to see available commands.")
            return 1
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 