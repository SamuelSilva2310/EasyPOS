import json
import os
import sys
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
        self.dirs = PlatformDirs("EasyPOS", "SAMUEL_LDA")

        # Create OS-appropriate directories
        self.data_dir = Path(self.dirs.user_data_dir)
        self.config_dir = Path(self.dirs.user_config_dir)
        self.log_dir = Path(self.dirs.user_log_dir)

        for p in [self.data_dir, self.config_dir, self.log_dir]:
            p.mkdir(parents=True, exist_ok=True)

        self.CONFIG_PATH = self.config_dir / "config.json"
        self.DB_PATH = self.data_dir / "easypos.db"
        self.LOG_PATH = self.log_dir / "easypos.log"

        print(f"[SETTINGS] CONFIG_PATH: {self.CONFIG_PATH}")
        print(f"[SETTINGS] DB_PATH: {self.DB_PATH}")
        print(f"[SETTINGS] LOG_PATH: {self.LOG_PATH}")
        self.settings = dict(AppSettings.DEFAULTS)
        self.load()

        print(f"[SETTINGS] RUNTIME_DIRECTORY: {self.RUNTIME_DIRECTORY}")

    @property
    def RUNTIME_DIRECTORY(self) -> Path:
        if getattr(sys, 'frozen', False):
            # PyInstaller runtime folder
            return Path(sys._MEIPASS).resolve()
        else:
            # Normal source layout
            return Path(__file__).resolve().parents[2]
        
    # ------------------------
    # Singleton
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
        if self.CONFIG_PATH.exists():
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    self._deep_update(self.settings, file_data)
            except Exception as e:
                print(f"⚠️ Failed to load config: {e}")
        else:
            self.save()

    def save(self):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save config: {e}")

    # ------------------------
    # Helpers
    # ------------------------
    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Update nested settings safely.
        Example:
            APP_SETTINGS.set("printer_connection_args.usb", {"idVendor": 1234})
        """
        keys = key.split(".")
        target = self.settings
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        if isinstance(value, dict) and isinstance(target.get(keys[-1]), dict):
            target[keys[-1]].update(value)
        else:
            target[keys[-1]] = value
        self.save()

    def _deep_update(self, base, updates):
        """Recursively merge dictionaries"""
        for k, v in updates.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                self._deep_update(base[k], v)
            else:
                base[k] = v

    def paths_summary(self):
        return {
            "config": str(self.CONFIG_PATH),
            "database": str(self.DB_PATH),
            "logs": str(self.LOG_PATH),
        }

# Global singleton
APP_SETTINGS = AppSettings.get_instance()