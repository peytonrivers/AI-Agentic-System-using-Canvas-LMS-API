import os
import requests
from requests import HTTPError, Response
from dotenv import load_dotenv

class CanvasClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("CANVAS_BASE_URL", "").rstrip("/")
        self.token = os.getenv("CANVAS_API_TOKEN")
        if not self.base_url or not self.token:
            raise ValueError("Missing CANVAS_BASE_URL or CANVAS_API_TOKEN")

    def get(self, endpoint: str, params=None):
        """Perform an authenticated GET request to Canvas."""
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()