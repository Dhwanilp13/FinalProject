#!/usr/bin/env python3
import os
import configparser


def load_db_config():
    """Read MySQL connection settings from settings.ini."""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "settings.ini not found. Copy settings.ini.example to settings.ini "
            "and add your database credentials."
        )

    config = configparser.ConfigParser()
    config.read(config_path)

    return {
        "host": config.get("database", "server").strip(),
        "user": config.get("database", "user").strip(),
        "password": config.get("database", "pass").strip(),
        "database": config.get("database", "name").strip(),
    }
