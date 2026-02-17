import os
import shlex
import socket
import subprocess
import time
import logging
from typing import Optional

import requests

logging.basicConfig(level=logging.INFO)


class OllamaManager:
    def __init__(self, host: str = "localhost", port: int = 11434, cmd: Optional[str] = None, auto_start: bool = True):
        self.host = host
        self.port = int(port)
        self.cmd = cmd
        self.auto_start = auto_start
        self.proc: Optional[subprocess.Popen] = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def is_running(self) -> bool:
        try:
            with socket.create_connection((self.host, self.port), timeout=1):
                return True
        except Exception:
            return False

    def start(self, timeout: int = 30) -> bool:
        if self.is_running():
            logging.info("Ollama already running")
            return True

        if not self.cmd:
            logging.warning("No Ollama command configured; cannot auto-start")
            return False

        args = shlex.split(self.cmd)
        logging.info("Starting Ollama with cmd: %s", self.cmd)
        try:
            self.proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            logging.exception("Failed to start Ollama process: %s", e)
            return False

        # Wait for the server port to accept connections
        start = time.time()
        while time.time() - start < timeout:
            if self.is_running():
                logging.info("Ollama started and accepting connections")
                return True
            time.sleep(0.5)

        logging.error("Ollama did not start within %s seconds", timeout)
        return False

    def stop(self, timeout: int = 5) -> None:
        if self.proc and self.proc.poll() is None:
            logging.info("Stopping Ollama process")
            try:
                self.proc.terminate()
                self.proc.wait(timeout=timeout)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass

        self.proc = None

    def generate(self, prompt: str, model: str = "phi3:mini", max_length: int = 512) -> str:
        if not self.is_running():
            if self.auto_start:
                started = self.start()
                if not started:
                    raise RuntimeError("Ollama not running and auto-start failed")
            else:
                raise RuntimeError("Ollama is not running")

        api_url = f"{self.url}/api/generate"
        payload = {"model": model, "prompt": prompt, "max_length": max_length}

        resp = requests.post(api_url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Common response fields
        if isinstance(data, dict):
            text = data.get("text") or data.get("response") or data.get("output")
            if text:
                return text
        return str(data)


def create_default_manager() -> OllamaManager:
    host = os.environ.get("OLLAMA_HOST", "localhost")
    port = int(os.environ.get("OLLAMA_PORT", 11434))
    cmd = os.environ.get("OLLAMA_CMD")  # e.g., "ollama serve --port 11434"
    auto = os.environ.get("OLLAMA_AUTO_START", "1") != "0"
    return OllamaManager(host=host, port=port, cmd=cmd, auto_start=auto)


if __name__ == "__main__":
    m = create_default_manager()
    if m.start():
        print("Ollama started")
    else:
        print("Failed to start Ollama")
