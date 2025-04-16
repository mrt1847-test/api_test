import requests

class BaseAPI:
    def __init__(self):
        self.BASE_URL = "https://dummyjson.com"

    def _get(self, endpoint):
        response = requests.get(f"{self.BASE_URL}{endpoint}")
        self._check_response(response)
        return response.json()

    def _post(self, endpoint, payload):
        response = requests.post(f"{self.BASE_URL}{endpoint}", json=payload)
        self._check_response(response)
        return response.json()

    def _put(self, endpoint, payload):
        response = requests.put(f"{self.BASE_URL}{endpoint}", json=payload)
        self._check_response(response)
        return response.json()

    def _delete(self, endpoint):
        response = requests.delete(f"{self.BASE_URL}{endpoint}")
        self._check_response(response)
        return response.json()

    def _check_response(self, response):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        return response