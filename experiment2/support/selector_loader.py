"""
Selector Loader - Loads XPath and CSS selectors from YAML files.

Similar to okrapods but using YAML format for easier maintenance.
All selectors are centralized in the selectors/ directory.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class SelectorLoader:
    """
    Loads and manages selectors from YAML files.
    
    Usage:
        selectors = SelectorLoader()
        selectors.load('common')  # loads selectors/common.yaml
        xpath = selectors.get('common', 'button')
    """
    
    _instance = None
    _selectors: Dict[str, Dict[str, Any]] = {}
    
    def __new__(cls):
        """Singleton pattern to ensure selectors are loaded once."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._selectors = {}
            cls._instance._load_all()
        return cls._instance
    
    @property
    def selectors_dir(self) -> Path:
        """Get the selectors directory path."""
        return Path(__file__).parent.parent / "selectors"
    
    def _load_all(self) -> None:
        """Load all YAML files from the selectors directory."""
        if not self.selectors_dir.exists():
            return
            
        for yaml_file in self.selectors_dir.glob("*.yaml"):
            name = yaml_file.stem
            self.load(name)
    
    def load(self, name: str) -> Dict[str, Any]:
        """
        Load a specific YAML selector file.
        
        Args:
            name: Name of the YAML file (without .yaml extension)
            
        Returns:
            Dictionary of selectors from the file
        """
        yaml_path = self.selectors_dir / f"{name}.yaml"
        
        if not yaml_path.exists():
            raise FileNotFoundError(f"Selector file not found: {yaml_path}")
        
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f) or {}
            
        self._selectors[name] = data
        return data
    
    def get(self, file: str, element: str, text: Optional[str] = None) -> str:
        """
        Get a selector from a loaded YAML file.
        
        Args:
            file: Name of the YAML file (without extension)
            element: Name of the element/selector
            text: Optional text to substitute for {TEXT} placeholder
            
        Returns:
            The selector string (XPath or CSS)
        """
        if file not in self._selectors:
            self.load(file)
            
        selectors = self._selectors.get(file, {})
        elements = selectors.get('elements', selectors)
        
        if element not in elements:
            raise KeyError(f"Element '{element}' not found in {file}.yaml")
        
        selector_data = elements[element]
        
        # Handle simple string selector
        if isinstance(selector_data, str):
            selector = selector_data
        # Handle dict with xpath/css keys
        elif isinstance(selector_data, dict):
            selector = selector_data.get('xpath') or selector_data.get('css', '')
        else:
            selector = str(selector_data)
        
        # Replace {TEXT} placeholder if text is provided
        if text and '{TEXT}' in selector:
            selector = selector.replace('{TEXT}', text)
            
        return selector
    
    def get_all(self, file: str) -> Dict[str, Any]:
        """Get all selectors from a file."""
        if file not in self._selectors:
            self.load(file)
        return self._selectors.get(file, {})
    
    def reload(self, file: Optional[str] = None) -> None:
        """Reload selector file(s)."""
        if file:
            self.load(file)
        else:
            self._selectors = {}
            self._load_all()


# Global instance for easy access
selectors = SelectorLoader()


def get_selector(file: str, element: str, text: Optional[str] = None) -> str:
    """
    Convenience function to get a selector.
    
    Args:
        file: Name of the YAML file (without extension)
        element: Name of the element
        text: Optional text for {TEXT} placeholder
        
    Returns:
        The selector string
        
    Example:
        xpath = get_selector('common', 'link', 'Click me')
        # Returns: //a[contains(text(), 'Click me')]
    """
    return selectors.get(file, element, text)
