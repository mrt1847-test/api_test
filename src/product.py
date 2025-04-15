import requests

class ProductApi():

    def __init__(self):
        self.BASE_URL = "https://dummyjson.com"

    def test_get_products(self):
        response = requests.get(f"{self.BASE_URL}/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert isinstance(data["products"], list)
        assert len(data["products"]) > 0

    def test_get_single_product(self):
        product_id = 1
        response = requests.get(f"{self.BASE_URL}/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert "title" in data

    def test_search_products(self):
        query = "phone"
        response = requests.get(f"{self.BASE_URL}/products/search?q={query}")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert query.lower() in product["title"].lower() or query.lower() in product["description"].lower()

    def test_add_product(self):
        payload = {
            "title": "Test Product",
            "price": 99,
            "description": "This is a test product",
            "category": "smartphones"
        }
        response = requests.post(f"{self.BASE_URL}/products/add", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["price"] == payload["price"]

    def test_update_product(self):
        update_data = {
            "price": 199
        }
        response = requests.put(f"{self.BASE_URL}/products/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == update_data["price"]

