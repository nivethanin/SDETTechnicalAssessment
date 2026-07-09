import requests

class APIClient:

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get(self, endpoint):
        return requests.get(f"{self.BASE_URL}{endpoint}")

    def post(self, endpoint, json):
        return requests.post(f"{self.BASE_URL}{endpoint}", json=json)

    def put(self, endpoint, json):
        return requests.put(f"{self.BASE_URL}{endpoint}", json=json)

    def patch(self, endpoint, json):
        return requests.patch(f"{self.BASE_URL}{endpoint}", json=json)

    def delete(self, endpoint):
        return requests.delete(f"{self.BASE_URL}{endpoint}")