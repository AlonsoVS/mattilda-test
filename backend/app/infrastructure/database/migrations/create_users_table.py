"""
Create users table for authentication.
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Insert a default admin user (password: admin123)
-- Password hash for 'admin123' using bcrypt
INSERT INTO users (username, email, hashed_password, full_name, is_active, is_superuser, created_at)
VALUES (
    'admin', 
    'admin@example.com', 
    '$2b$12$FPLrBRKIIu4A2MIozFyGSO8TvgbgNjoJWAbiZ7nfEvVtK5LCUkory', 
    'System Administrator', 
    TRUE, 
    TRUE,
    CURRENT_TIMESTAMP
) ON CONFLICT (username) DO NOTHING;
"""

DROP_USERS_TABLE = """
DROP TABLE IF EXISTS users;
"""
