import json
import os
import threading

# CONFIG_LOCATION = os.path.join(os.path.expanduser("~"), ".easypos_config.json")
CONIFIG_LOCATION = 'easypos_config.json'


class AppSettings:
    _instance = None
    _lock = threading.Lock()

    DEFAULTS = {
        "theme": "dark",
        "printer_connection_type": "usb",

        "printer_connection_args": {

            "usb": {
                "idVendor": 1046,
                "idProduct": 20497,
            },
            "lan": {
                "ip": "237.84.2.178",
                "port": 9100
            },
            "fake": {

            }
        }
    }

    CONFIG_PATH = CONIFIG_LOCATION

    def __init__(self):
        self.settings = dict(AppSettings.DEFAULTS)
        self.load()

    @classmethod
    def get_instance(cls):
        """Singleton accessor"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = AppSettings()
        return cls._instance

    def load(self):
        """Loads settings from file (if exists)"""
        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r") as f:
                    file_data = json.load(f)
                    self.settings.update(file_data)
            except Exception as e:
                print(f"⚠️ Failed to load config: {e}")
        else:
            self.save()

    def save(self):
        """Persists settings to disk"""
        try:
            with open(self.CONFIG_PATH, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"⚠️ Failed to save config: {e}")

    # --- Helper accessors ---
    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
