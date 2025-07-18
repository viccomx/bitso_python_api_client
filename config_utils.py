import json
import os
from typing import Dict, Optional


class ConfigUtils:
    """Utility class for managing configuration files"""

    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict:
        """
        Load configuration from config.json file

        Args:
            config_path: Optional path to config file. If not provided, looks in same directory

        Returns:
            Dict: Configuration data

        Raises:
            FileNotFoundError: If config.json is not found
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "config.json not found. Please copy config.template.json to config.json and fill in your credentials."
            )

        with open(config_path, "r") as f:
            return json.load(f)
