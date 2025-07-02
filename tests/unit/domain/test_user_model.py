"""
Unit tests for User domain model.
"""

import pytest
from datetime import datetime
from app.domain.models.user import User


class TestUserModel:
    """Test cases for User domain model."""

    def test_user_creation_with_valid_data(self):
        """Test creating a user with valid data."""
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.id is None
        assert user.created_at is None
        assert user.updated_at is None

    def test_user_creation_with_minimal_data(self):
        """Test creating a user with minimal required data."""
        user = User(
            username="testuser",
            email="test@example.com"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name is None
        assert user.is_active is True
        assert user.is_superuser is False

    def test_user_creation_with_all_data(self):
        """Test creating a user with all data including timestamps."""
        created_at = datetime.now()
        updated_at = datetime.now()
        
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            is_active=False,
            is_superuser=True,
            id=1,
            created_at=created_at,
            updated_at=updated_at
        )
        
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is False
        assert user.is_superuser is True
        assert user.created_at == created_at
        assert user.updated_at == updated_at

    def test_user_validation_empty_username(self):
        """Test validation fails for empty username."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username="", email="test@example.com")

    def test_user_validation_whitespace_username(self):
        """Test validation fails for whitespace-only username."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username="   ", email="test@example.com")

    def test_user_validation_short_username(self):
        """Test validation fails for username too short."""
        with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
            User(username="ab", email="test@example.com")

    def test_user_validation_long_username(self):
        """Test validation fails for username too long."""
        long_username = "a" * 51
        with pytest.raises(ValueError, match="Username cannot exceed 50 characters"):
            User(username=long_username, email="test@example.com")

    def test_user_validation_invalid_email(self):
        """Test validation fails for invalid email."""
        with pytest.raises(ValueError, match="Valid email is required"):
            User(username="testuser", email="invalid-email")

    def test_user_validation_empty_email(self):
        """Test validation fails for empty email."""
        with pytest.raises(ValueError, match="Valid email is required"):
            User(username="testuser", email="")

    def test_user_validation_long_email(self):
        """Test validation fails for email too long."""
        long_email = "a" * 90 + "@example.com"  # Over 100 chars
        with pytest.raises(ValueError, match="Email cannot exceed 100 characters"):
            User(username="testuser", email=long_email)

    def test_user_validation_long_full_name(self):
        """Test validation fails for full name too long."""
        long_name = "a" * 101
        with pytest.raises(ValueError, match="Full name cannot exceed 100 characters"):
            User(username="testuser", email="test@example.com", full_name=long_name)

    def test_user_deactivate(self):
        """Test user deactivation."""
        user = User(username="testuser", email="test@example.com")
        assert user.is_active is True
        
        user.deactivate()
        assert user.is_active is False

    def test_user_activate(self):
        """Test user activation."""
        user = User(username="testuser", email="test@example.com", is_active=False)
        assert user.is_active is False
        
        user.activate()
        assert user.is_active is True

    def test_promote_to_superuser(self):
        """Test promoting user to superuser."""
        user = User(username="testuser", email="test@example.com")
        assert user.is_superuser is False
        
        user.promote_to_superuser()
        assert user.is_superuser is True

    def test_demote_from_superuser(self):
        """Test demoting user from superuser."""
        user = User(username="testuser", email="test@example.com", is_superuser=True)
        assert user.is_superuser is True
        
        user.demote_from_superuser()
        assert user.is_superuser is False

    def test_update_profile_email(self):
        """Test updating user profile email."""
        user = User(username="testuser", email="old@example.com")
        
        user.update_profile(email="new@example.com")
        assert user.email == "new@example.com"

    def test_update_profile_full_name(self):
        """Test updating user profile full name."""
        user = User(username="testuser", email="test@example.com")
        
        user.update_profile(full_name="New Name")
        assert user.full_name == "New Name"

    def test_update_profile_both_fields(self):
        """Test updating both email and full name."""
        user = User(username="testuser", email="old@example.com", full_name="Old Name")
        
        user.update_profile(email="new@example.com", full_name="New Name")
        assert user.email == "new@example.com"
        assert user.full_name == "New Name"

    def test_update_profile_invalid_email(self):
        """Test update profile fails with invalid email."""
        user = User(username="testuser", email="test@example.com")
        
        with pytest.raises(ValueError, match="Valid email is required"):
            user.update_profile(email="invalid-email")

    def test_update_profile_long_email(self):
        """Test update profile fails with email too long."""
        user = User(username="testuser", email="test@example.com")
        long_email = "a" * 90 + "@example.com"
        
        with pytest.raises(ValueError, match="Email cannot exceed 100 characters"):
            user.update_profile(email=long_email)

    def test_update_profile_long_full_name(self):
        """Test update profile fails with full name too long."""
        user = User(username="testuser", email="test@example.com")
        long_name = "a" * 101
        
        with pytest.raises(ValueError, match="Full name cannot exceed 100 characters"):
            user.update_profile(full_name=long_name)

    def test_update_profile_empty_string_full_name(self):
        """Test update profile allows empty string for full name."""
        user = User(username="testuser", email="test@example.com", full_name="Old Name")
        
        user.update_profile(full_name="")
        assert user.full_name == ""

    def test_update_profile_none_values(self):
        """Test update profile ignores None values."""
        user = User(username="testuser", email="old@example.com", full_name="Old Name")
        
        user.update_profile(email=None, full_name=None)
        assert user.email == "old@example.com"
        assert user.full_name == "Old Name"
