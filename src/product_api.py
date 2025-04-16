from src.base_api import BaseAPI

class ProductAPI(BaseAPI):
    def test_get_products(self):
        data = self._get("/products")
        assert "products" in data
        assert isinstance(data["products"], list)
        assert len(data["products"]) > 0

    def test_get_single_product(self):
        product_id = 1
        data = self._get(f"/products/{product_id}")
        assert data["id"] == product_id
        assert "title" in data

    def test_search_products(self):
        query = "phone"
        data = self._get(f"/products/search?q={query}")
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
        data = self._post("/products/add", payload)
        assert data["title"] == payload["title"]
        assert data["price"] == payload["price"]

    def test_update_product(self):
        update_data = {
            "price": 199
        }
        data = self._put("/products/1", update_data)
        assert data["price"] == update_data["price"]

