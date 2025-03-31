"""PyEnvBuilder - A tool for managing Python virtual environments in Xcode projects."""

import os
import sys
import subprocess
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

def create_xcode_script(project_path: str) -> Tuple[bool, Optional[str]]:
    """Create a shell script for setting up Python environment in Xcode projects.
    
    Args:
        project_path: Path to the Xcode project directory
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        project_dir = Path(project_path).resolve()
        if not project_dir.exists():
            return False, f"Project directory does not exist: {project_dir}"
            
        # Create the script content
        script_content = f"""#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/{config.get('env_name', 'BuildEnv')}" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$SCRIPT_DIR/{config.get('env_name', 'BuildEnv')}"
fi

# Activate virtual environment
source "$SCRIPT_DIR/{config.get('env_name', 'BuildEnv')}/bin/activate"

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
fi

# Keep the virtual environment activated
exec "$SHELL"
"""
        
        # Write the script
        script_path = project_dir / "setup_python_env.sh"
        script_path.write_text(script_content)
        
        # Make the script executable
        os.chmod(script_path, 0o755)
        
        logger.info(f"Created Xcode build script at {script_path}")
        return True, None
        
    except Exception as e:
        error_msg = f"Failed to create Xcode script: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def setup_xcode_project(project_path: str) -> Tuple[bool, Optional[str]]:
    """Set up a Python environment for an Xcode project.
    
    Args:
        project_path: Path to the Xcode project directory
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        # Run pre-installation checks
        success, messages = run_all_checks(project_path)
        for msg in messages:
            if msg.startswith("✓"):
                logger.info(msg)
            else:
                logger.error(msg)
        if not success:
            return False, "Pre-installation checks failed"
            
        # Create virtual environment
        success, error_msg = create_env(project_path)
        if not success:
            return False, error_msg
            
        # Create Xcode script
        success, error_msg = create_xcode_script(project_path)
        if not success:
            return False, error_msg
            
        logger.info("Successfully set up Python environment for Xcode project")
        return True, None
        
    except Exception as e:
        error_msg = f"Failed to set up Xcode project: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

__version__ = "0.1.0" 