# SECRET_KEY Configuration Guide

This document explains how the SECRET_KEY is configured for JWT authentication in the Mattilda API.

## 🔐 Security Overview

The SECRET_KEY is used for:
- JWT token signing and verification
- Ensuring token integrity and authenticity
- Preventing token forgery

## 📁 File Structure

```
app/core/
├── auth.py          # Uses SECRET_KEY from settings
├── config.py        # Loads SECRET_KEY from environment
└── dependencies.py  # Uses auth functions

.env                 # Development SECRET_KEY
.env.prod           # Production SECRET_KEY (keep secret!)
```

## ⚙️ Configuration

### 1. Environment Variables

The SECRET_KEY is loaded from environment variables in this order:

1. **Environment variable**: `SECRET_KEY`
2. **Fallback**: `"dev-secret-key-change-in-production"`

### 2. Configuration Files

**Development (.env):**
```bash
SECRET_KEY=H51GZkhlCS5sieAzodPcCGl_EOcMTJmw8W9XHcovZEo
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Production (.env.prod):**
```bash
SECRET_KEY=-ormV8rjsudu2CdmD1maIh9RO_rpXJXehrPNSD9EBOUeBHP3pZ94SJqdXUoAOvY4A1dKY7mNpHr51xcOWAeBeQ
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### 3. Code Implementation

**app/core/config.py:**
```python
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
```

**app/core/auth.py:**
```python
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
```

## 🔧 How to Generate New SECRET_KEY

### For Development:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### For Production:
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 🚀 Deployment Considerations

### Development
- Uses 32-character SECRET_KEY
- Token expires in 30 minutes
- Stored in `.env` file

### Production
- Uses 64-character SECRET_KEY
- Token expires in 15 minutes (more secure)
- Stored in `.env.prod` file
- **NEVER commit production keys to version control!**

### Docker Deployment
```bash
# Set SECRET_KEY as environment variable
docker run -e SECRET_KEY="your-production-secret-key" your-app

# Or use docker-compose with .env.prod
docker-compose --env-file .env.prod up
```

### Server Deployment
```bash
# Set environment variable
export SECRET_KEY="your-production-secret-key"

# Or load from file
source .env.prod
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔍 Testing Configuration

Run the test script to verify configuration:
```bash
python test_secret_key.py
```

Expected output:
```
✅ SECRET_KEY is properly loaded from .env file
✅ JWT functionality works correctly
🎉 SUCCESS! Using secure SECRET_KEY from environment variable
```

## 🛡️ Security Best Practices

1. **Use Strong Keys**: Minimum 32 characters, preferably 64+
2. **Keep Secret**: Never log or expose SECRET_KEY
3. **Rotate Regularly**: Change SECRET_KEY periodically
4. **Environment Specific**: Different keys for dev/staging/prod
5. **Secure Storage**: Use secrets managers in production

## ⚠️ Important Notes

- Changing SECRET_KEY invalidates all existing JWT tokens
- Users will need to log in again after key rotation
- Store production keys securely (AWS Secrets Manager, Azure Key Vault, etc.)
- Never commit SECRET_KEY to version control

## 🔧 Troubleshooting

### Issue: "Invalid token" errors after deployment
**Solution**: Check if SECRET_KEY changed between environments

### Issue: Tokens not working
**Solution**: Verify SECRET_KEY is loaded correctly:
```python
from app.core.config import settings
print(f"SECRET_KEY: {settings.SECRET_KEY[:10]}...")
```

### Issue: Environment variable not loaded
**Solution**: Ensure `.env` file is in project root and python-dotenv is installed
