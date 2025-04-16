import requests

class CartAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create(self, data):
        return requests.post(f"{self.base_url}/products/add", json=data)

    def read(self, product_id):
        return requests.get(f"{self.base_url}/products/{product_id}")

    def update(self, product_id, data):
        return requests.put(f"{self.base_url}/products/{product_id}", json=data)

    def delete(self, product_id):
        return requests.delete(f"{self.base_url}/products/{product_id}")

    # 새로 추가된 API 엔드포인트
    def search(self, query):
        return requests.get(f"{self.base_url}/products/search?q={query}")