import time
import socket
from langchain_openai import ChatOpenAI

class LocalLLM:
    """
    A wrapper on top of the exposed Foundational Model present on Apple devices.
    Automatically waits for the local server to be ready before returning a model.
    """
    def __init__(self, base_url="http://localhost:8080/api/v1", model="base", wait_timeout=5):
        self.base_url = base_url
        self.model_name = model
        self.wait_timeout = wait_timeout
        self._model_instance = None
        self._host = "localhost"
        self._port = 8080

    def _wait_for_service(self):
        """Polls the port until it's open or timeout is reached."""
        start_time = time.time()
        while time.time() - start_time < self.wait_timeout:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((self._host, self._port)) == 0:
                    return True
            time.sleep(1) 
        return False

    def get_model(self):
        """
        Ensures the service is running before returning the model instance.
        Caches the instance once created.
        """
        if self._model_instance:
            return self._model_instance

        if not self._wait_for_service():
            raise ConnectionError(
                f"Timeout: AppleIntelligenceApi not detected on {self._host}:{self._port} "
                f"after {self.wait_timeout}s. Is the Swift process running?"
            )

        self._model_instance = ChatOpenAI(
            base_url=self.base_url,
            api_key="not-needed", # type: ignore
            model=self.model_name,
        )
        return self._model_instance