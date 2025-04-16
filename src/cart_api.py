from src.base_api import BaseAPI


class CartAPI(BaseAPI):

    def test_get_all_carts(self):
        data = self._get("/carts")
        assert "carts" in data
        assert isinstance(data["carts"], list)

    def test_get_cart_by_id(self):
        cart_id = 1
        data = self._get(f"/carts/{cart_id}")
        assert data["id"] == cart_id
        assert "products" in data

    def test_get_user_cart(self):
        user_id = 5
        data = self._get(f"/carts/user/{user_id}")
        assert isinstance(data["carts"], list)

    def test_add_cart(self):
        payload = {
            "userId": 1,
            "products": [
                {"id": 1, "quantity": 2},
                {"id": 50, "quantity": 1}
            ]
        }
        data = self._post("/carts/add", payload)
        assert data["userId"] == payload["userId"]
        assert len(data["products"]) == len(payload["products"])

    def test_update_cart(self):
        cart_id = 1
        payload = {
            "products": [
                {"id": 1, "quantity": 3}
            ]
        }
        data = self._put(f"/carts/{cart_id}", payload)
        assert isinstance(data["products"], list)
        assert data["products"][0]["quantity"] == 3

    def test_delete_cart(self):
        # 실제 삭제가 되진 않지만 dummyjson은 200 응답을 반환합니다.
        cart_id = 1
        data = self._delete(f"/carts/{cart_id}")
        assert "isDeleted" in data
        assert data["isDeleted"] is True