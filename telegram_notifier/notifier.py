# telegram_notifier/notifier.py

import requests
import time
import os
from enum import Enum
import importlib.resources as pkg_resources

class NotifierStatus(Enum):
    INITIALIZED = "initialized"
    STARTED = "started"
    FINISHED = "finished"
    ERROR = "error"

class Notifier:
    def __init__(self, simulation_name, tokens: dict = None, env_file=None):
        if tokens is not None:
            self.bot_token = tokens.get("BOT_TOKEN")
            self.chat_id = tokens.get("CHAT_ID")
        else:
            if env_file is None:
                with pkg_resources.path(__package__, '.env') as path:
                    env_file = str(path)

            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

            self.bot_token = os.getenv("BOT_TOKEN")
            self.chat_id = os.getenv("CHAT_ID")

        self.simulation_name: str = f"`{simulation_name:s}`"
        self.status: NotifierStatus = NotifierStatus.INITIALIZED
        self.error_message = None
        self.exception_propagation: bool = False
        self.start_time = None
        self.end_time = None

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload)
        return response.json()

    def start_notification(self):
        message = f"Simulation : {self.simulation_name} has started."
        self.send_message(message)

    def finish_notification(self, duration=None):
        if duration is None:
            message = f"Simulation : {self.simulation_name} has finished successfully!"
        else:
            message = f"Simulation : {self.simulation_name} has finished successfully! Duration: {duration:.1f} seconds."
        self.send_message(message)

    def error_notificaiton(self, error_message):
        message = f"Simulation : {self.simulation_name} encountered an error: {error_message}"
        self.send_message(message)

    def __enter__(self):
        self.status = NotifierStatus.STARTED
        self.start_time = time.time()
        self.start_notification()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        if exc_type is not None:
            self.status = NotifierStatus.ERROR
            self.error_message = str(exc_val)
            self.error_notificaiton(self.error_message)
        else:
            self.status = NotifierStatus.FINISHED
            self.finish_notification(duration)
        return self.exception_propagation
