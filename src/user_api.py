from src.base_api import BaseAPI

class UserAPI(BaseAPI):

    def test_get_all_users(self):
        data = self._get("/users")
        assert "users" in data
        assert isinstance(data["users"], list)

    def test_get_single_user(self):
        user_id = 1
        data = self._get(f"/users/{user_id}")
        assert data["id"] == user_id
        assert "firstName" in data

    def test_search_users(self):
        query = "John"
        data = self._get(f"/users/search?q={query}")
        assert "users" in data
        for user in data["users"]:
            full_name = f"{user['firstName']} {user['lastName']}".lower()
            assert query.lower() in full_name

    def test_add_user(self):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "age": 30,
            "gender": "male",
            "email": "test.user@example.com",
            "username": "testuser123",
            "password": "password"
        }
        data = self._post("/users/add", payload)
        assert data["firstName"] == payload["firstName"]
        assert data["username"] == payload["username"]

    def test_update_user(self):
        user_id = 1
        payload = {
            "lastName": "Updated"
        }
        data = self._put(f"/users/{user_id}", payload)
        assert data["lastName"] == payload["lastName"]

    def test_delete_user(self):
        user_id = 1
        data = self._delete(f"/users/{user_id}")
        assert "isDeleted" in data
        assert data["isDeleted"] is True