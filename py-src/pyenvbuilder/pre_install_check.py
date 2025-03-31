"""Pre-installation checks for Xcode Python environment setup."""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple

from .config import config

logger = logging.getLogger(__name__)

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version meets requirements.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    required_version = tuple(map(int, config.get("python_version", "3.6").split(".")))
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        return False, f"Python {'.'.join(map(str, required_version))} or higher is required"
    return True, f"✓ Python version {'.'.join(map(str, current_version))} meets requirements"

def check_venv_available() -> Tuple[bool, str]:
    """Check if venv module is available.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        import venv
        return True, "✓ venv module is available"
    except ImportError:
        return False, "venv module is not available"

def check_pip_available() -> Tuple[bool, str]:
    """Check if pip is available and working.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            capture_output=True,
            text=True
        )
        return True, f"✓ pip is available and working (version: {result.stdout.strip()})"
    except subprocess.CalledProcessError:
        return False, "pip is not available or not working"

def check_xcode_command_line_tools() -> Tuple[bool, str]:
    """Check if Xcode Command Line Tools are installed.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        result = subprocess.run(
            ["xcode-select", "-p"],
            check=True,
            capture_output=True,
            text=True
        )
        return True, f"✓ Xcode Command Line Tools are installed at {result.stdout.strip()}"
    except subprocess.CalledProcessError:
        return False, "Xcode Command Line Tools are not installed"

def check_project_directory(project_path: str) -> Tuple[bool, str]:
    """Check if project directory is valid and secure.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        path = Path(project_path).resolve()
        
        # Check if directory exists
        if not path.exists():
            return False, f"Project directory does not exist: {project_path}"
            
        # Check if it's a directory
        if not path.is_dir():
            return False, f"Project path is not a directory: {project_path}"
            
        # Check for path traversal attempts
        if ".." in str(path):
            return False, "Invalid project path: path traversal detected"
            
        # Check directory permissions
        if not os.access(path, os.R_OK | os.W_OK):
            return False, f"Insufficient permissions for project directory: {project_path}"
            
        return True, f"✓ Project directory {project_path} is valid and secure"
        
    except Exception as e:
        return False, f"Invalid project path: {str(e)}"

def check_system_dependencies() -> Tuple[bool, str]:
    """Check if required system dependencies are installed.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    required_tools = ["git", "make", "gcc"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        return False, f"Missing required system dependencies: {', '.join(missing_tools)}"
    return True, "✓ All required system dependencies are installed"

def run_all_checks(project_path: str) -> Tuple[bool, List[str]]:
    """Run all pre-installation checks.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Tuple[bool, List[str]]: (success, messages)
    """
    checks = [
        check_python_version(),
        check_venv_available(),
        check_pip_available(),
        check_xcode_command_line_tools(),
        check_project_directory(project_path),
        check_system_dependencies()
    ]
    
    success = all(check[0] for check in checks)
    messages = [check[1] for check in checks]
    
    return success, messages 