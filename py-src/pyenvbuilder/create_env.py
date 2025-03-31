"""Create a Python virtual environment for Xcode projects."""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Tuple

from .config import config

logger = logging.getLogger(__name__)

def install_requirements(python_path: Path, requirements: List[str]) -> Tuple[bool, Optional[str]]:
    """Install Python requirements.
    
    Args:
        python_path: Path to Python executable
        requirements: List of requirements to install
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        # Build pip install command
        cmd = [str(python_path), "-m", "pip", "install"]
        
        # Add options based on configuration
        if config.get("no_cache", True):
            cmd.append("--no-cache-dir")
            
        # Add requirements
        cmd.extend(requirements)
        
        # Run pip install
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        logger.info("Successfully installed requirements")
        return True, None
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to install requirements: {e.stderr}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error installing requirements: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def create_env(project_path: str, env_name: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Create a Python virtual environment for an Xcode project.
    
    Args:
        project_path: Path to the Xcode project directory
        env_name: Optional name of the virtual environment (default: from config)
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        project_dir = Path(project_path).resolve()
        if not project_dir.exists():
            return False, f"Project directory does not exist: {project_dir}"
            
        # Use provided env_name or get from config
        env_name = env_name or config.get("env_name", "BuildEnv")
        env_path = project_dir / env_name
        
        if env_path.exists():
            return False, f"Environment already exists: {env_path}"
            
        # Create virtual environment
        logger.info(f"Creating virtual environment at {env_path}")
        subprocess.run(
            [sys.executable, "-m", "venv", str(env_path)],
            check=True,
            capture_output=True
        )
        
        # Get the path to the virtual environment's Python executable
        if sys.platform == "win32":
            python_path = env_path / "Scripts" / "python.exe"
        else:
            python_path = env_path / "bin" / "python"
            
        # Upgrade pip
        logger.info("Upgrading pip...")
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        
        # Install basic requirements
        logger.info("Installing basic requirements...")
        requirements = config.get("requirements", [])
        
        success, error_msg = install_requirements(python_path, requirements)
        if not success:
            return False, error_msg
        
        # Create requirements.txt if it doesn't exist
        requirements_file = project_dir / "requirements.txt"
        if not requirements_file.exists():
            requirements_file.write_text("\n".join(requirements))
            
        logger.info(f"Successfully created virtual environment at {env_path}")
        return True, None
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to create virtual environment: {e.stderr}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def get_env_python(project_path: str, env_name: Optional[str] = None) -> Tuple[Optional[Path], Optional[str]]:
    """Get the path to the Python executable in the virtual environment.
    
    Args:
        project_path: Path to the Xcode project directory
        env_name: Optional name of the virtual environment (default: from config)
        
    Returns:
        Tuple[Optional[Path], Optional[str]]: (python_path, error_message)
    """
    try:
        project_dir = Path(project_path).resolve()
        
        # Use provided env_name or get from config
        env_name = env_name or config.get("env_name", "BuildEnv")
        env_path = project_dir / env_name
        
        if not env_path.exists():
            return None, f"Environment does not exist: {env_path}"
            
        if sys.platform == "win32":
            python_path = env_path / "Scripts" / "python.exe"
        else:
            python_path = env_path / "bin" / "python"
            
        if not python_path.exists():
            return None, f"Python executable not found at {python_path}"
            
        return python_path, None
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

