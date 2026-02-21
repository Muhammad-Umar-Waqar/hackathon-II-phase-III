import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db, Base
import os

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAuthEndpoints:
    """Integration tests for authentication endpoints"""

    def test_register_user_success(self, test_db):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data

    def test_register_duplicate_email(self, test_db):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser1",
                "password": "SecurePass123!"
            }
        )

        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 409
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, test_db):
        """Test registration with duplicate username"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test1@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )

        # Second registration with same username
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test2@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 409
        assert "Username already taken" in response.json()["detail"]

    def test_login_success(self, test_db):
        """Test successful login"""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            params={
                "email": "test@example.com",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    def test_login_wrong_password(self, test_db):
        """Test login with wrong password"""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            params={
                "email": "test@example.com",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, test_db):
        """Test login with non-existent user"""
        response = client.post(
            "/api/v1/auth/login",
            params={
                "email": "nonexistent@example.com",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 401

    def test_get_current_user(self, test_db):
        """Test getting current user information"""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            params={
                "email": "test@example.com",
                "password": "SecurePass123!"
            }
        )
        token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_current_user_invalid_token(self, test_db):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestTaskEndpoints:
    """Integration tests for task endpoints"""

    def get_auth_token(self):
        """Helper method to register and login a user"""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            params={
                "email": "test@example.com",
                "password": "SecurePass123!"
            }
        )
        return login_response.json()["access_token"]

    def test_create_task_success(self, test_db):
        """Test successful task creation"""
        token = self.get_auth_token()

        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "status": "pending"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["status"] == "pending"
        assert "id" in data

    def test_create_task_invalid_status(self, test_db):
        """Test task creation with invalid status"""
        token = self.get_auth_token()

        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "status": "invalid_status"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400

    def test_create_task_unauthorized(self, test_db):
        """Test task creation without authentication"""
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "status": "pending"
            }
        )
        assert response.status_code == 403

    def test_get_tasks(self, test_db):
        """Test retrieving all tasks for a user"""
        token = self.get_auth_token()

        # Create multiple tasks
        for i in range(3):
            client.post(
                "/api/v1/tasks/",
                json={
                    "title": f"Task {i}",
                    "description": f"Description {i}",
                    "status": "pending"
                },
                headers={"Authorization": f"Bearer {token}"}
            )

        # Get all tasks
        response = client.get(
            "/api/v1/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_task_by_id(self, test_db):
        """Test retrieving a specific task"""
        token = self.get_auth_token()

        # Create a task
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "status": "pending"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"

    def test_get_task_not_found(self, test_db):
        """Test retrieving a non-existent task"""
        token = self.get_auth_token()

        response = client.get(
            "/api/v1/tasks/999",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404

    def test_update_task(self, test_db):
        """Test updating a task"""
        token = self.get_auth_token()

        # Create a task
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Original Title",
                "description": "Original Description",
                "status": "pending"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]

        # Update the task
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={
                "title": "Updated Title",
                "status": "completed"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "completed"

    def test_delete_task(self, test_db):
        """Test deleting a task"""
        token = self.get_auth_token()

        # Create a task
        create_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "status": "pending"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 404

    def test_user_isolation(self, test_db):
        """Test that users can only access their own tasks"""
        # Create first user and task
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user1@example.com",
                "username": "user1",
                "password": "SecurePass123!"
            }
        )
        login1 = client.post(
            "/api/v1/auth/login",
            params={"email": "user1@example.com", "password": "SecurePass123!"}
        )
        token1 = login1.json()["access_token"]

        create_response = client.post(
            "/api/v1/tasks/",
            json={"title": "User 1 Task", "status": "pending"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # Create second user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "username": "user2",
                "password": "SecurePass123!"
            }
        )
        login2 = client.post(
            "/api/v1/auth/login",
            params={"email": "user2@example.com", "password": "SecurePass123!"}
        )
        token2 = login2.json()["access_token"]

        # Try to access user1's task with user2's token
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 404  # Should not find the task
