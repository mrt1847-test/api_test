# conftest.py
import pytest
from api.product_api import ProductAPI
from api.cart_api import CartAPI
from api.user_api import UserAPI

@pytest.fixture(scope="session")
def base_url():
    return "https://dummyjson.com"

# ProductAPI 관련 fixture
@pytest.fixture(scope="module")
def product_api(base_url):
    return ProductAPI(base_url)

@pytest.fixture(scope="module")
def product_data():
    return {
        "title": "Template Test Product",
        "price": 777,
        "description": "Product created from CDPR test template"
    }

@pytest.fixture(scope="module")
def created_product(product_api, product_data):
    response = product_api.create(product_data)
    assert response.status_code == 200
    return response.json()

# CartAPI 관련 fixture
@pytest.fixture(scope="module")
def cart_api(base_url):
    return CartAPI(base_url)

@pytest.fixture(scope="module")
def cart_data():
    return {
        "product_id": 1,  # 예시 값, 실제로는 product id와 연결됨
        "quantity": 1
    }

@pytest.fixture(scope="module")
def created_cart(cart_api, cart_data):
    response = cart_api.add_to_cart(cart_data["product_id"])
    assert response.status_code == 200
    return response.json()

# UserAPI 관련 fixture
@pytest.fixture(scope="module")
def user_api(base_url):
    return UserAPI(base_url)

@pytest.fixture(scope="module")
def user_data():
    return {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }

@pytest.fixture(scope="module")
def created_user(user_api, user_data):
    response = user_api.create(user_data)
    assert response.status_code == 200
    return response.json()