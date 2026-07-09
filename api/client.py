import requests

class APIClient:

    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT_SECONDS = 10

    def get(self, endpoint):
        return requests.get(f"{self.BASE_URL}{endpoint}", timeout=self.TIMEOUT_SECONDS)

    def post(self, endpoint, json):
        return requests.post(f"{self.BASE_URL}{endpoint}", json=json, timeout=self.TIMEOUT_SECONDS)

    def put(self, endpoint, json):
        return requests.put(f"{self.BASE_URL}{endpoint}", json=json, timeout=self.TIMEOUT_SECONDS)

    def patch(self, endpoint, json):
        return requests.patch(f"{self.BASE_URL}{endpoint}", json=json, timeout=self.TIMEOUT_SECONDS)

    def delete(self, endpoint):
        return requests.delete(f"{self.BASE_URL}{endpoint}", timeout=self.TIMEOUT_SECONDS)