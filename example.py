import pytest
import requests
import time
# API 기본 URL (환경 변수나 설정 파일에서 가져오는 것이 좋음)
BASE_URL = "http://api.example.com" # 실제 테스트 대상 URL로 변경하세요.
VALID_TOKEN = "Bearer your_valid_token" # 실제 유효한 토큰으로 변경
INVALID_TOKEN = "Bearer invalid_token"
ADMIN_TOKEN = "Bearer your_admin_token" # 관리자 권한 토큰 (인가 테스트용)
USER_TOKEN = "Bearer your_user_token" # 일반 사용자 토큰 (인가 테스트용)
# --- Fixtures (테스트 데이터 및 설정) ---
@pytest.fixture(scope="module") # 모듈 단위로 실행, 아이템 생성/삭제 관리
def created_item():
    """테스트용 아이템을 생성하고 ID를 반환하며, 테스트 후 삭제합니다."""
    headers = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "Test Item Fixture", "price": 99.99}
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 201
    item_data = response.json()
    item_id = item_data.get("id")
    yield item_id # 테스트 함수에 item_id 전달
    # --- Teardown ---
    # 테스트 완료 후 생성된 아이템 삭제 (항상 실행되도록 보장)
    if item_id:
        delete_headers = {"Authorization": VALID_TOKEN}
        requests.delete(f"{BASE_URL}/items/{item_id}", headers=delete_headers)
        print(f"\nCleaned up item with ID: {item_id}")
# --- 1. 기능적 정확성 (Functional Correctness) ---
def test_create_item_happy_path():
    """(POST /items) 정상적인 아이템 생성 테스트"""
    headers = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "New Gadget", "price": 120.50}
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 201 # 생성 성공 확인
    data = response.json()
    assert "id" in data # 응답에 id 필드가 있는지 확인
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    # 생성된 아이템은 테스트 후 정리 필요 (fixture 활용 추천)
    # 여기서는 간단히 예시, 실제로는 fixture로 관리하거나 teardown 로직 추가
    if "id" in data:
         requests.delete(f"{BASE_URL}/items/{data['id']}", headers={"Authorization": VALID_TOKEN})
def test_get_item_happy_path(created_item):
    """(GET /items/{item_id}) 특정 아이템 조회 성공 테스트"""
    item_id = created_item # fixture 로부터 생성된 아이템 ID 받기
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item Fixture" # fixture 에서 생성한 이름
    assert data["price"] == 99.99        # fixture 에서 생성한 가격
def test_get_items_list():
    """(GET /items) 전체 아이템 목록 조회 테스트 (최소 1개 이상 있다고 가정)"""
    response = requests.get(f"{BASE_URL}/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) # 응답이 리스트 형태인지 확인
    # assert len(data) > 0 # 데이터가 실제로 있는지 확인 (선택적)
def test_update_item_happy_path(created_item):
    """(PUT /items/{item_id}) 아이템 수정 성공 테스트"""
    item_id = created_item
    headers = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "Updated Test Item", "price": 150.00}
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == payload["name"] # 수정된 이름 확인
    assert data["price"] == payload["price"] # 수정된 가격 확인
def test_delete_item_happy_path():
    """(DELETE /items/{item_id}) 아이템 삭제 성공 테스트"""
    # 삭제할 아이템 먼저 생성
    headers_create = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload_create = {"name": "Item to Delete", "price": 10.0}
    response_create = requests.post(f"{BASE_URL}/items", json=payload_create, headers=headers_create)
    assert response_create.status_code == 201
    item_id_to_delete = response_create.json()["id"]
    # 삭제 요청
    headers_delete = {"Authorization": VALID_TOKEN}
    response_delete = requests.delete(f"{BASE_URL}/items/{item_id_to_delete}", headers=headers_delete)
    assert response_delete.status_code == 204 # No Content 확인
    # 삭제 확인 (조회 시 404가 나와야 함)
    response_get = requests.get(f"{BASE_URL}/items/{item_id_to_delete}")
    assert response_get.status_code == 404
@pytest.mark.parametrize("method", ["GET", "PUT", "PATCH", "DELETE"])
def test_invalid_method_on_items_root(method):
    """(/{items}) 루트 경로에 허용되지 않은 메소드 요청 테스트"""
    response = requests.request(method, f"{BASE_URL}/items")
    # POST, GET 외에는 405 Method Not Allowed 예상 (API 설계에 따라 다름)
    if method not in ["GET", "POST"]:
        assert response.status_code == 405
# --- 2. 응답 검증 (Response Validation) ---
def test_get_item_response_schema(created_item):
    """(GET /items/{item_id}) 응답 본문 스키마(구조) 검증"""
    item_id = created_item
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    # 기본적인 키 존재 여부 확인
    assert "id" in data
    assert "name" in data
    assert "price" in data
    # 필요시 jsonschema 라이브러리로 더 엄격하게 검증 가능
    # from jsonschema import validate
    # schema = { ... } # 예상 스키마 정의
    # validate(instance=data, schema=schema)
def test_get_items_content_type_header():
    """(GET /items) 응답 헤더 Content-Type 검증"""
    response = requests.get(f"{BASE_URL}/items")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/json" # 또는 "application/json; charset=utf-8" 등
# --- 3. 오류 처리 (Error Handling) ---
def test_create_item_missing_required_field():
    """(POST /items) 필수 필드 누락 시 400 Bad Request 테스트"""
    headers = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "Incomplete Item"} # 'price' 필드 누락
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 400
    # assert "Price is required" in response.text # 구체적인 오류 메시지 확인 (선택적)
def test_get_nonexistent_item():
    """(GET /items/{item_id}) 존재하지 않는 아이템 조회 시 404 Not Found 테스트"""
    non_existent_id = "non_existent_id_12345"
    response = requests.get(f"{BASE_URL}/items/{non_existent_id}")
    assert response.status_code == 404
@pytest.mark.parametrize("invalid_price", [-10, 0, "not_a_number"])
def test_create_item_invalid_price(invalid_price):
    """(POST /items) 유효하지 않은 가격 값으로 생성 시 400 Bad Request 테스트"""
    headers = {"Authorization": VALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "Invalid Price Item", "price": invalid_price}
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 400
# --- 4. 인증 및 인가 (Authentication & Authorization) ---
def test_create_item_no_auth():
    """(POST /items) 인증 없이 아이템 생성 시 401 Unauthorized 테스트"""
    headers = {"Content-Type": "application/json"} # Authorization 헤더 없음
    payload = {"name": "Unauthorized Item", "price": 50.0}
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 401
def test_create_item_invalid_token():
    """(POST /items) 유효하지 않은 토큰으로 아이템 생성 시 401 Unauthorized 테스트"""
    headers = {"Authorization": INVALID_TOKEN, "Content-Type": "application/json"}
    payload = {"name": "Invalid Token Item", "price": 60.0}
    response = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    assert response.status_code == 401
@pytest.mark.skip(reason="인가 테스트는 실제 환경과 역할 설정에 따라 달라짐") # 예시로 스킵 처리
def test_delete_item_forbidden(created_item):
    """(DELETE /items/{item_id}) 일반 사용자 권한으로 삭제 시 403 Forbidden 테스트"""
    item_id = created_item
    # 일반 사용자 토큰 사용 (관리자 권한이 없다고 가정)
    headers = {"Authorization": USER_TOKEN}
    response = requests.delete(f"{BASE_URL}/items/{item_id}", headers=headers)
    assert response.status_code == 403 # 권한 없음 확인
# --- 5. 성능 및 부하 (Performance & Load - 기본 수준) ---
def test_get_items_response_time():
    """(GET /items) 응답 시간 기본 체크 (1초 미만)"""
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/items")
    end_time = time.time()
    duration = end_time - start_time
    assert response.status_code == 200
    assert duration < 1.0 # 응답 시간이 1초 미만인지 확인 (기준은 요구사항에 따라 조절)
    print(f"\nGET /items response time: {duration:.4f} seconds")
# --- 6. 상태 관리 (State Management) ---
# 이 부분은 보통 fixture 나 여러 테스트 함수에 걸쳐서 검증합니다.
# 위 test_delete_item_happy_path 에서 생성->삭제->조회(404) 과정을 통해
# 상태 변경(삭제됨)을 검증하는 로직이 포함되어 있습니다.
# test_update_item_happy_path 에서도 생성(fixture)->수정->검증 과정을 통해 상태 변경을 확인합니다.
# --- 추가: Mocking 예시 (외부 API 의존성 제거) ---
# from unittest.mock import patch
# def test_process_item_with_external_service(mocker):
#     """외부 서비스 호출 부분을 Mocking 하여 테스트"""
#     # mocker fixture (pytest-mock) 또는 unittest.mock.patch 사용
#     mock_response = requests.Response()
#     mock_response.status_code = 200
#     mock_response._content = b'{"external_data": "mocked"}'
#     mocker.patch('requests.get', return_value=mock_response)
#     # 테스트하려는 함수 호출 (이 함수 내부에서 requests.get을 사용한다고 가정)
#     result = your_module.process_item_using_external_api("some_id")
#     assert result == "processed_with_mocked_data"