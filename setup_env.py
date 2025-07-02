#!/usr/bin/env python3
"""
Environment setup helper for Mattilda project.
This script helps users understand and choose the right environment configuration.
"""

import os
import sys
import shutil
from pathlib import Path


def print_header():
    print("🌍 Mattilda Environment Configuration Helper")
    print("=" * 50)


def print_env_info():
    print("\n📋 Available Environment Configurations:")
    print()
    
    print("1. 🏠 Local Development (.env.local)")
    print("   - Run application directly on your machine")
    print("   - Requires local PostgreSQL installation")
    print("   - Best for: Quick development, debugging")
    print("   - Database: localhost:5432")
    print("   - Usage: python -m uvicorn app.main:app --reload")
    print()
    
    print("2. 🐳 Docker Development (.env.docker)")
    print("   - Run application in Docker containers")
    print("   - Includes PostgreSQL container")
    print("   - Best for: Consistent environment, team development")
    print("   - Database: Docker service 'db'")
    print("   - Usage: make dev")
    print()
    
    print("3. 🚀 Docker Production (.env.prod)")
    print("   - Production-ready Docker deployment")
    print("   - Optimized for security and performance")
    print("   - Best for: Production deployment")
    print("   - Database: Docker service 'db'")
    print("   - Usage: make prod")


def check_files():
    project_root = Path(__file__).parent
    env_files = {
        'local': project_root / '.env.local',
        'docker': project_root / '.env.docker',
        'prod': project_root / '.env.prod',
        'default': project_root / '.env'
    }
    
    print("\n📁 Environment File Status:")
    for name, path in env_files.items():
        status = "✅ Found" if path.exists() else "❌ Missing"
        print(f"   {name:8} ({path.name}): {status}")
    
    return env_files


def show_current_config():
    current_env = os.getenv('ENVIRONMENT', 'unknown')
    database_url = os.getenv('DATABASE_URL', 'not set')
    debug = os.getenv('DEBUG', 'not set')
    
    print(f"\n🔧 Current Configuration:")
    print(f"   Environment: {current_env}")
    print(f"   Debug Mode:  {debug}")
    print(f"   Database:    {database_url}")


def copy_env_file(source_name, env_files):
    source_file = env_files.get(source_name)
    target_file = env_files['default']
    
    if not source_file.exists():
        print(f"❌ Source file {source_file} not found!")
        return False
    
    try:
        shutil.copy2(source_file, target_file)
        print(f"✅ Copied {source_file.name} to {target_file.name}")
        return True
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return False


def interactive_setup():
    print("\n🔧 Interactive Environment Setup")
    print("Choose your development environment:")
    print("1. Local Development (no Docker)")
    print("2. Docker Development")
    print("3. Docker Production")
    print("4. Show current configuration")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    env_files = check_files()
    
    if choice == '1':
        if copy_env_file('local', env_files):
            print("\n🏠 Local development environment configured!")
            print("Next steps:")
            print("1. Make sure PostgreSQL is running locally")
            print("2. Run: python -m uvicorn app.main:app --reload")
            print("3. Access: http://localhost:8000")
    
    elif choice == '2':
        print("\n🐳 Docker development environment is ready!")
        print("Next steps:")
        print("1. Run: make dev")
        print("2. Access: http://localhost:8000")
        print("3. View logs: make logs")
    
    elif choice == '3':
        print("\n🚀 Docker production environment selected!")
        print("⚠️  IMPORTANT: Update .env.prod with secure values:")
        print("   - Change DATABASE_PASSWORD")
        print("   - Set strong SECRET_KEY")
        print("   - Configure ALLOWED_ORIGINS")
        print("Next steps:")
        print("1. Edit .env.prod with production values")
        print("2. Run: make prod")
    
    elif choice == '4':
        show_current_config()
    
    elif choice == '5':
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice. Please try again.")
        interactive_setup()


def main():
    print_header()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['info', 'help', '--help', '-h']:
            print_env_info()
        elif command == 'check':
            check_files()
        elif command == 'status':
            show_current_config()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: info, check, status")
    else:
        print_env_info()
        interactive_setup()


if __name__ == "__main__":
    main()
