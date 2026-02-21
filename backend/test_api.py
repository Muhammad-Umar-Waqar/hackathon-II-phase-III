"""
Simple API test script to verify backend endpoints
Run this after starting the backend server
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_register():
    """Test user registration"""
    print("\n=== Testing Registration ===")
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Password123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 201, 409]  # 409 if already exists
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n=== Testing Login ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "test@example.com",
        "password": "Password123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        if response.status_code == 200:
            return result.get("access_token")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_create_task(token):
    """Test task creation"""
    print("\n=== Testing Create Task ===")
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_tasks(token):
    """Test getting all tasks"""
    print("\n=== Testing Get Tasks ===")
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 50)
    print("Backend API Test Suite")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")

    # Test registration
    if not test_register():
        print("\n❌ Registration test failed!")
        return

    # Test login
    token = test_login()
    if not token:
        print("\n❌ Login test failed!")
        return

    print(f"\n✅ Got access token: {token[:20]}...")

    # Test create task
    if not test_create_task(token):
        print("\n❌ Create task test failed!")
        return

    # Test get tasks
    if not test_get_tasks(token):
        print("\n❌ Get tasks test failed!")
        return

    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
