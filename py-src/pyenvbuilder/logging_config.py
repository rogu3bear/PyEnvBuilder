"""Logging configuration for PyEnvBuilder."""

import os
import logging
from pathlib import Path
from typing import Optional

def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO) -> None:
    """Set up logging configuration for PyEnvBuilder.
    
    Args:
        log_file: Optional path to log file
        level: Logging level (default: INFO)
    """
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create handlers
    handlers = [
        logging.StreamHandler()
    ]
    
    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add new handlers
    for handler in handlers:
        handler.setFormatter(console_formatter)
        root_logger.addHandler(handler)
    
    # Suppress verbose logging from third-party libraries
    logging.getLogger('pip').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING) 