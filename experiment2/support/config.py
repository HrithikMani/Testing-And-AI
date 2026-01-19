"""
Configuration settings for WebChart test automation.

This module provides centralized configuration for:
- WebChart URL and credentials
- Browser settings
- Timeouts and wait times
- Test environment settings

Usage:
    from support.config import config
    
    page.goto(config.WEBCHART_URL)
    login(config.USERNAME, config.PASSWORD)
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class WebChartConfig:
    """WebChart application configuration."""
    
    # WebChart URL - can be overridden via environment variable
    BASE_URL: str = os.environ.get(
        'WEBCHART_URL', 
        'https://zeus.med-web.com/webchart/wcthkonda/webchart.cgi'
    )
    
    # Login credentials - ALWAYS use environment variables in production
    USERNAME: str = os.environ.get('WEBCHART_USERNAME', 'selenium')
    PASSWORD: str = os.environ.get('WEBCHART_PASSWORD', 'selenium')
    
    # Login method: 'standard' or 'miedev'
    LOGIN_METHOD: str = os.environ.get('WEBCHART_LOGIN_METHOD', 'standard')
    
    # Browser configuration
    HEADLESS: bool = os.environ.get('HEADLESS', 'false').lower() == 'true'
    SLOW_MO: int = int(os.environ.get('SLOW_MO', '0'))
    
    # Viewport settings
    VIEWPORT_WIDTH: int = int(os.environ.get('VIEWPORT_WIDTH', '1280'))
    VIEWPORT_HEIGHT: int = int(os.environ.get('VIEWPORT_HEIGHT', '720'))
    
    # Timeout settings (in milliseconds)
    DEFAULT_TIMEOUT: int = int(os.environ.get('DEFAULT_TIMEOUT', '30000'))
    AJAX_TIMEOUT: int = int(os.environ.get('AJAX_TIMEOUT', '10000'))
    ANIMATION_WAIT: float = float(os.environ.get('ANIMATION_WAIT', '1.0'))
    AUTOCOMPLETE_DELAY: int = int(os.environ.get('AUTOCOMPLETE_DELAY', '50'))
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE: bool = os.environ.get('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    SCREENSHOT_DIR: str = os.environ.get('SCREENSHOT_DIR', 'reports/screenshots')
    
    # Trace settings
    TRACE_ON_FAILURE: bool = os.environ.get('TRACE_ON_FAILURE', 'false').lower() == 'true'
    TRACE_DIR: str = os.environ.get('TRACE_DIR', 'reports/traces')
    
    # Video recording
    RECORD_VIDEO: bool = os.environ.get('RECORD_VIDEO', 'false').lower() == 'true'
    VIDEO_DIR: str = os.environ.get('VIDEO_DIR', 'reports/videos')


@dataclass  
class TestEnvironment:
    """Test environment settings."""
    
    # Environment name (dev, staging, prod)
    ENV_NAME: str = os.environ.get('TEST_ENV', 'dev')
    
    # Debug mode
    DEBUG: bool = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Retry failed tests
    RETRY_FAILED: int = int(os.environ.get('RETRY_FAILED', '0'))
    
    # Parallel execution
    PARALLEL_WORKERS: int = int(os.environ.get('PARALLEL_WORKERS', '1'))


# Global configuration instances
config = WebChartConfig()
env = TestEnvironment()


def get_webchart_url(path: str = '') -> str:
    """
    Get full WebChart URL with optional path.
    
    Args:
        path: Optional path to append (e.g., '?f=admin')
        
    Returns:
        Full URL string
    """
    base = config.BASE_URL.rstrip('/')
    if path:
        if not path.startswith('?') and not path.startswith('/'):
            path = '/' + path
        return f"{base}{path}"
    return base


def update_config(**kwargs):
    """
    Update configuration values dynamically.
    
    Args:
        **kwargs: Configuration values to update
        
    Example:
        update_config(USERNAME='newuser', PASSWORD='newpass')
    """
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        elif hasattr(env, key):
            setattr(env, key, value)
        else:
            raise ValueError(f"Unknown configuration key: {key}")
