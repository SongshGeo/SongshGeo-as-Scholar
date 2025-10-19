#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
Centralized logging configuration for publication management scripts.

Uses loguru for structured logging with automatic rotation and retention.
"""

from pathlib import Path
from loguru import logger
import sys

# Log directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOG_DIR / "publications.log"


def setup_logger(script_name: str, verbose: bool = False):
    """
    Setup logger for a script.
    
    Args:
        script_name: Name of the script calling this function
        verbose: If True, also output to console
    
    Returns:
        Configured logger instance
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler if verbose
    if verbose:
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> <level>{level: <5}</level> <level>{message}</level>",
            level="INFO",
            colorize=True
        )
    
    # Add file handler with rotation and retention
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} {level: <5} {message}",
        level="INFO",
        rotation="10 MB",  # Rotate when file reaches 10MB
        retention="3 months",  # Keep logs for 3 months
        compression="zip",  # Compress rotated logs
        enqueue=True,  # Thread-safe
    )
    
    # Bind script name to all log records
    return logger.bind(script=script_name)


def log_section(log: logger, title: str):
    """Log a section separator."""
    log.info(f"--- {title} ---")


def log_success(log: logger, message: str):
    """Log a success message."""
    log.success(f"✅ {message}")


def log_warning(log: logger, message: str):
    """Log a warning message."""
    log.warning(f"⚠️  {message}")


def log_error(log: logger, message: str):
    """Log an error message."""
    log.error(f"❌ {message}")


def log_info(log: logger, message: str, indent: int = 0):
    """Log an info message with optional indentation."""
    prefix = "   " * indent
    log.info(f"{prefix}{message}")

