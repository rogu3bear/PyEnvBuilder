"""Clean up Python virtual environments for Xcode projects."""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Optional, Tuple

from .config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_valid_venv(path: Path) -> Tuple[bool, Optional[str]]:
    """Check if a directory is a valid virtual environment.
    
    Args:
        path: Path to check
        
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    try:
        # Check if path exists
        if not path.exists():
            return False, f"Path does not exist: {path}"
            
        # Check if it's a directory
        if not path.is_dir():
            return False, f"Path is not a directory: {path}"
            
        # Check for path traversal attempts
        if ".." in str(path):
            return False, "Invalid path: path traversal detected"
            
        # Check for Python executable
        if sys.platform == "win32":
            python_path = path / "Scripts" / "python.exe"
        else:
            python_path = path / "bin" / "python"
            
        if not python_path.exists():
            return False, f"Python executable not found at {python_path}"
            
        # Check if it's actually a virtual environment
        try:
            import venv
            venv.check_venv(str(path))
            return True, None
        except Exception as e:
            return False, f"Not a valid virtual environment: {str(e)}"
            
    except Exception as e:
        return False, f"Error checking virtual environment: {str(e)}"

def cleanup_env(env_path: str, force: Optional[bool] = None) -> Tuple[bool, Optional[str]]:
    """Clean up a Python virtual environment.
    
    Args:
        env_path: Path to the virtual environment
        force: Optional force flag (default: from config)
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        env_dir = Path(env_path).resolve()
        
        # Validate virtual environment
        is_valid, error_msg = is_valid_venv(env_dir)
        if not is_valid:
            return False, error_msg
            
        # Use provided force flag or get from config
        force = force if force is not None else config.get("force_cleanup", False)
        
        # Confirm cleanup unless force is True
        if not force:
            response = input(f"Are you sure you want to delete {env_dir}? [y/N] ")
            if response.lower() != "y":
                logger.info("Cleanup cancelled")
                return True, None
                
        # Check if environment is active
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            current_venv = Path(sys.prefix).resolve()
            if current_venv == env_dir:
                return False, "Cannot delete currently active virtual environment"
                
        # Remove the environment
        logger.info(f"Removing virtual environment at {env_dir}")
        shutil.rmtree(env_dir)
        
        logger.info("Cleanup completed successfully")
        return True, None
        
    except Exception as e:
        error_msg = f"Failed to clean up environment: {str(e)}"
        logger.error(error_msg)
        return False, error_msg