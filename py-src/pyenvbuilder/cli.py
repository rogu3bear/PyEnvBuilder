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

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="PyEnvBuilder - A tool for managing Python virtual environments in Xcode projects"
    )
    
    parser.add_argument(
        "--project-path",
        type=str,
        default=os.getcwd(),
        help="Path to the Xcode project directory"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force cleanup without confirmation"
    )
    
    parser.add_argument(
        "--env-name",
        type=str,
        help="Name of the virtual environment (default: BuildEnv)"
    )
    
    parser.add_argument(
        "--python-version",
        type=str,
        help="Required Python version (default: 3.6)"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Update configuration with command line arguments
    if args.env_name:
        config.set("env_name", args.env_name)
    if args.python_version:
        config.set("python_version", args.python_version)
    
    project_path = Path(args.project_path).resolve()
    
    try:
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
            
        logger.info("Successfully set up Python environment")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 