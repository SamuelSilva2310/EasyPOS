import json
import os
import threading
from pathlib import Path
from platformdirs import PlatformDirs

import logging
logger = logging.getLogger(__name__)

class AppSettings:
    _instance = None
    _lock = threading.Lock()

    DEFAULTS = {
        "title": "EasyPOS",
        "images_directory": "images",
        "theme": "dark",
        "printer_connection_type": "usb",
        "printer_connection_args": {
            "usb": {
                "idVendor": 1046,
                "idProduct": 20497,
                "encoding": "cp860",
            },
            "network": {
                "ip": "237.84.2.178",
                "port": 9100,
                "encoding": "cp860",
            },
            "fake": {}
        },
    }

    def __init__(self):
        # Use OS-appropriate paths
        self.dirs = PlatformDirs("EasyPOS", "SAMUE_LDA")

        # --- Base folders ---
        self.data_dir = Path(self.dirs.user_data_dir)
        self.config_dir = Path(self.dirs.user_config_dir)
        self.log_dir = Path(self.dirs.user_log_dir)

        # --- Ensure they exist ---
        for p in [self.data_dir, self.config_dir, self.log_dir]:
            p.mkdir(parents=True, exist_ok=True)

        # --- Core files ---
        self.CONFIG_PATH = self.config_dir / "config.json"
        self.DB_PATH = self.data_dir / "easypos.db"
        self.LOG_PATH = self.log_dir / "easypos.log"

        # --- Internal state ---
        self.settings = dict(AppSettings.DEFAULTS)
        self.load()

        print(f"[INFO] Paths: {self.paths_summary()}")
        print(f"[INFO] Settings: {self.settings}")

    # ------------------------
    # Singleton access
    # ------------------------
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = AppSettings()
        return cls._instance

    # ------------------------
    # Persistence
    # ------------------------
    def load(self):
        """Load settings from JSON config"""
        if self.CONFIG_PATH.exists():
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    self.settings.update(file_data)
            except Exception as e:
                print(f"⚠️ Failed to load config: {e}")
        else:
            self.save()

    def save(self):
        """Save settings to disk"""
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save config: {e}")

    # ------------------------
    # Accessors
    # ------------------------
    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    # ------------------------
    # Helpers
    # ------------------------
    def paths_summary(self):
        return {
            "config": str(self.CONFIG_PATH),
            "database": str(self.DB_PATH),
            "logs": str(self.LOG_PATH),
        }


# Global singleton
APP_SETTINGS = AppSettings.get_instance()