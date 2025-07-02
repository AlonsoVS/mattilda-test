# Mattilda Test Project

A modern school management system built with FastAPI, PostgreSQL, and clean architecture principles.

## 🏗️ Architecture

This project implements **Domain-Driven Design (DDD)** and **Clean Architecture** principles to create a maintainable, testable, and scalable application. The architecture emphasizes separation of concerns, dependency inversion, and business logic isolation.

### 🎯 **Architectural Principles**

#### **Domain-Driven Design (DDD)**
- **Domain Focus**: Business logic is central to the application design
- **Ubiquitous Language**: Consistent terminology between developers and domain experts
- **Bounded Contexts**: Clear boundaries between different business domains
- **Domain Models**: Rich domain objects that encapsulate business rules

#### **Clean Architecture (Hexagonal Architecture)**
- **Dependency Rule**: Dependencies point inward toward the domain
- **Framework Independence**: Business logic doesn't depend on frameworks
- **Database Independence**: Domain layer is agnostic to data storage
- **UI Independence**: Business logic can work with any interface
- **Testability**: Business logic can be tested without external dependencies

## 🏗️ Project Structure

```
mattilda-test/
├── app/
│   ├── core/                 # Configuration and utilities
│   ├── domain/              # Domain models and business logic
│   │   ├── models/          # Domain entities
│   │   ├── repositories/    # Repository interfaces
│   │   └── enums.py         # Domain enums
│   ├── application/         # Application layer
│   │   ├── dtos/           # Data transfer objects
│   │   └── services/       # Application services
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── database/       # Database connection
│   │   ├── persistence/    # Database entities
│   │   ├── repositories/   # Repository implementations
│   │   └── mappers/        # Domain/Entity mappers
│   └── presentation/        # Presentation layer
│       └── api/v1/         # API controllers
├── tests/
│   └── unit/domain/        # Domain model tests
├── docker/                 # Docker configuration
├── Dockerfile             # Development container
├── Dockerfile.prod        # Production container
├── docker-compose.yml     # Development orchestration
├── docker-compose.prod.yml # Production orchestration
├── Makefile              # Convenience commands
└── requirements.txt      # Python dependencies
```

### 🏛️ **Layer Structure**

```
app/
├── 🎯 domain/         # Pure business logic (innermost layer)
├── 🔧 application/    # Application services and use cases  
├── 🏗️ infrastructure/ # External adapters and implementations
├── 🎨 presentation/   # Controllers and API layer
└── ⚙️ core/          # Cross-cutting concerns and configuration
```

### 📁 **Detailed Layer Breakdown**

#### 🎯 **Domain Layer** (`app/domain/`)
*The heart of the application - contains pure business logic*

**Purpose**: Encapsulates business rules, entities, and domain logic without any external dependencies.

**Structure**:
```
domain/
├── models/           # Domain entities (pure Python dataclasses)
│   ├── school.py     # School business entity with validation
│   ├── student.py    # Student business entity with rules
│   ├── invoice.py    # Invoice business entity with calculations
│   └── user.py       # User business entity with authentication 
|
├── repositories/     # Abstract repository interfaces
│   ├── school_repository.py     # School persistence contract
│   ├── student_repository.py    # Student persistence contract
│   ├── invoice_repository.py    # Invoice persistence contract
│   └── user_repository.py       # User persistence contract
└── enums.py         # Business enumerations (InvoiceStatus, PaymentMethod)
```

**Key Characteristics**:
- ✅ **Pure Python**: No framework dependencies (FastAPI, SQLModel, etc.)
- ✅ **Business Rules**: Validation and business logic in `__post_init__` methods
- ✅ **Immutable Interfaces**: Repository interfaces define contracts without implementation
- ✅ **Rich Domain Models**: Entities with behavior, not just data containers
- ✅ **Framework Agnostic**: Can be used with any web framework or database

**Example Domain Model**:
```python
@dataclass
class School:
    name: str
    address: str
    # ... other fields
    
    def __post_init__(self):
        """Business rule validation"""
        if not self.name.strip():
            raise ValueError("School name cannot be empty")
        if self.established_year < 1800:
            raise ValueError("Invalid establishment year")
    
    def deactivate(self) -> None:
        """Business operation"""
        self.is_active = False
```

#### 🔧 **Application Layer** (`app/application/`)
*Orchestrates domain objects to fulfill use cases*

**Purpose**: Contains application-specific business rules and orchestrates domain objects to fulfill use cases.

**Structure**:
```
application/
├── services/         # Application services (use cases)
│   ├── school_service.py     # School business operations
│   ├── student_service.py    # Student business operations  
│   ├── invoice_service.py    # Invoice business operations
│   └── auth_service.py       # Authentication operations
└── dtos/            # Data Transfer Objects
    ├── school_dto.py         # School API contracts
    ├── student_dto.py        # Student API contracts
    ├── invoice_dto.py        # Invoice API contracts
    └── auth_dto.py           # Authentication contracts
```

**Key Characteristics**:
- ✅ **Use Case Implementation**: Implements specific business workflows
- ✅ **Domain Orchestration**: Coordinates multiple domain entities
- ✅ **Transaction Management**: Handles business transaction boundaries
- ✅ **DTO Pattern**: Defines data contracts for external communication
- ✅ **Dependency Injection**: Depends on domain interfaces, not implementations

#### 🏗️ **Infrastructure Layer** (`app/infrastructure/`)
*Implements external adapters and technical details*

**Purpose**: Provides implementations for domain interfaces and handles all external concerns.

**Structure**:
```
infrastructure/
├── persistence/      # Database entities (SQLModel)
│   ├── school_entity.py      # School database mapping
│   ├── student_entity.py     # Student database mapping
│   ├── invoice_entity.py     # Invoice database mapping
│   └── user_entity.py        # User database mapping
├── repositories/     # Repository implementations
│   ├── school_repository.py  # School data access implementation
│   ├── student_repository.py # Student data access implementation
│   ├── invoice_repository.py # Invoice data access implementation
│   └── user_repository.py    # User data access implementation
├── mappers/         # Domain ↔ Persistence mapping
│   ├── school_mapper.py      # School entity conversion
│   ├── student_mapper.py     # Student entity conversion
│   ├── invoice_mapper.py     # Invoice entity conversion
│   └── user_mapper.py        # User entity conversion
└── database/        # Database configuration
    ├── connection.py         # Database connection setup
    ├── seed_data.py          # Initial data population
    └── migrations/           # Database schema changes
```

**Key Characteristics**:
- ✅ **Dependency Implementation**: Implements domain repository interfaces
- ✅ **Data Persistence**: Handles database operations with SQLModel/SQLAlchemy
- ✅ **Entity Mapping**: Converts between domain models and database entities
- ✅ **External Services**: Integrates with databases, APIs, file systems
- ✅ **Framework Specific**: Contains framework-dependent code (FastAPI, SQLModel)

#### 🎨 **Presentation Layer** (`app/presentation/`)
*Handles HTTP requests and API concerns*

**Purpose**: Manages HTTP communication, request/response handling, and API documentation.

**Structure**:
```
presentation/
└── api/v1/          # API version 1
    ├── school_controller.py  # School HTTP endpoints
    ├── student_controller.py # Student HTTP endpoints
    ├── invoice_controller.py # Invoice HTTP endpoints
    ├── auth_controller.py    # Authentication endpoints
    ├── cache_controller.py   # Cache management endpoints
    └── api.py               # API router configuration
```

**Key Characteristics**:
- ✅ **HTTP Protocol**: Handles HTTP requests/responses
- ✅ **API Documentation**: OpenAPI/Swagger documentation generation
- ✅ **Authentication**: JWT token validation and authorization
- ✅ **Validation**: Request/response validation with Pydantic
- ✅ **Error Handling**: HTTP status codes and error responses

#### ⚙️ **Core Layer** (`app/core/`)
*Cross-cutting concerns and configuration*

**Purpose**: Provides shared utilities, configuration, and cross-cutting concerns.

**Structure**:
```
core/
├── config.py        # Environment configuration
├── auth.py          # Authentication utilities
├── dependencies.py  # Dependency injection setup
├── pagination.py    # Pagination utilities
└── cache.py         # Caching utilities
```

**Key Characteristics**:
- ✅ **Configuration Management**: Environment variables and settings
- ✅ **Security**: JWT authentication and password hashing
- ✅ **Dependency Injection**: FastAPI dependency providers
- ✅ **Shared Utilities**: Pagination, caching, validation helpers

### 🔄 **Data Flow Architecture**

```
HTTP Request → Presentation → Application → Domain ← Infrastructure
     ↓              ↓            ↓          ↓         ↓
1. API Controller   2. Service    3. Domain   4. Repository
2. Validate Request 3. Business   4. Business 5. Database
3. Call Service     4. Logic      5. Rules    6. Entity Mapping
4. Return Response  5. Orchestrate 6. Validate 7. Data Persistence
```

### 🎯 **Benefits of This Architecture**

#### **Maintainability**
- **Separation of Concerns**: Each layer has a single responsibility
- **Loose Coupling**: Dependencies point inward, enabling easy changes
- **Clear Boundaries**: Well-defined interfaces between layers

#### **Testability**  
- **Unit Testing**: Domain logic tested without external dependencies
- **Mocking**: Repository interfaces easily mocked for testing
- **Integration Testing**: Each layer can be tested independently

#### **Scalability**
- **Plugin Architecture**: Easy to add new features without affecting existing code
- **Technology Independence**: Can switch databases or frameworks without changing business logic
- **Microservices Ready**: Clear boundaries make it easy to extract services

#### **Business Alignment**
- **Domain Focus**: Business logic is explicit and central
- **Ubiquitous Language**: Code reflects business terminology
- **Business Rule Centralization**: All business rules in domain layer

### 🛠️ **Implementation Patterns**

#### **Repository Pattern**
- Abstract data access behind interfaces
- Domain defines contracts, infrastructure implements them
- Enables testing without database dependencies

#### **Mapper Pattern**  
- Converts between domain models and database entities
- Keeps domain pure from persistence concerns
- Enables different persistence strategies

#### **Dependency Injection**
- Dependencies injected from outer layers
- Follows dependency inversion principle
- Enables easy testing and flexibility

#### **DTO Pattern**
- Defines data contracts for API communication
- Separates internal models from external representation
- Enables API versioning and evolution

### 💡 **Real-World Architecture Benefits**

#### **Example 1: Changing Database Technology**
```python
# ❌ Without Clean Architecture: Database logic scattered throughout
def get_school(school_id: int):
    # Direct database calls mixed with business logic
    query = "SELECT * FROM schools WHERE id = ?"
    result = db.execute(query, school_id)
    # Business validation mixed with data access
    if result.established_year < 1800:
        raise ValueError("Invalid year")
    return result

# ✅ With Clean Architecture: Easy database changes
# Domain layer (unchanged when switching databases)
@dataclass
class School:
    def __post_init__(self):
        if self.established_year < 1800:
            raise ValueError("Invalid year")

# Infrastructure layer (only this changes when switching DB)
class SchoolRepository:
    def get_by_id(self, school_id: int) -> School:
        # Can switch from PostgreSQL to MongoDB without affecting domain
        entity = self.session.get(SchoolEntity, school_id)
        return SchoolMapper.to_domain(entity)
```

#### **Example 2: Unit Testing Business Logic**
```python
# ❌ Without Clean Architecture: Hard to test
def create_invoice(student_id: int, amount: float):
    # Requires database connection to test
    student = db.get_student(student_id)
    if student.grade_level < 1:
        raise ValueError("Invalid grade")
    # Creates database record during test
    return db.create_invoice(student_id, amount)

# ✅ With Clean Architecture: Easy unit testing
@dataclass  
class Invoice:
    def __post_init__(self):
        # Pure business logic - no database needed
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
    
    def calculate_total_with_tax(self, tax_rate: float) -> float:
        # Pure calculation - easily testable
        return self.amount * (1 + tax_rate)

# Test (no database required)
def test_invoice_calculation():
    invoice = Invoice(amount=100.0, student_id=1)
    assert invoice.calculate_total_with_tax(0.1) == 110.0
```

#### **Example 3: Adding New Features**
```python
# ✅ Adding email notifications without changing existing code

# 1. Domain layer: Add new business rule (if needed)
@dataclass
class Invoice:
    def mark_as_paid(self) -> None:
        if self.status == InvoiceStatus.PAID:
            raise ValueError("Invoice already paid")
        self.status = InvoiceStatus.PAID
        # Domain event could be added here

# 2. Application layer: Add notification use case
class InvoiceService:
    def __init__(self, repo: InvoiceRepository, notifier: EmailNotifier):
        self.repo = repo
        self.notifier = notifier
    
    async def mark_invoice_paid(self, invoice_id: int):
        invoice = await self.repo.get_by_id(invoice_id)
        invoice.mark_as_paid()  # Domain business rule
        await self.repo.update(invoice)
        await self.notifier.send_payment_confirmation(invoice)  # New feature

# 3. Infrastructure layer: Add email implementation
class EmailNotifier:
    async def send_payment_confirmation(self, invoice: Invoice):
        # Email sending logic
        pass

# 4. Presentation layer: No changes needed!
# Existing API endpoints automatically support the new feature
```

#### **Example 4: API Versioning**
```python
# ✅ Supporting multiple API versions with same business logic

# Domain layer: Unchanged
@dataclass
class School:
    name: str
    address: str
    # Business logic stays the same

# Application layer: Unchanged  
class SchoolService:
    async def create_school(self, school: School) -> School:
        # Business operations stay the same
        return await self.repo.create(school)

# Presentation layer: Different DTOs per version
# V1 API
class SchoolCreateDTOV1(BaseModel):
    name: str
    address: str

# V2 API (with additional fields)
class SchoolCreateDTOV2(BaseModel):
    name: str
    address: str
    principal_email: str  # New field
    
# Both versions use the same service layer!
```

### 🔍 **Code Organization Example**

Here's how a complete feature flows through the architecture:

```python
# 1. 🎯 DOMAIN LAYER - Pure business logic
@dataclass
class Student:
    name: str
    grade_level: int
    school_id: int
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name is required")
        if self.grade_level < 1 or self.grade_level > 12:
            raise ValueError("Grade must be 1-12")
    
    def promote_to_next_grade(self) -> None:
        if self.grade_level >= 12:
            raise ValueError("Cannot promote beyond grade 12")
        self.grade_level += 1

# 2. 🔧 APPLICATION LAYER - Use cases
class StudentService:
    def __init__(self, student_repo: StudentRepository, school_repo: SchoolRepository):
        self.student_repo = student_repo
        self.school_repo = school_repo
    
    async def enroll_student(self, student_data: StudentCreateDTO) -> Student:
        # Validate school exists
        school = await self.school_repo.get_by_id(student_data.school_id)
        if not school:
            raise ValueError("School not found")
        
        # Create domain object (triggers validation)
        student = Student(
            name=student_data.name,
            grade_level=student_data.grade_level,
            school_id=student_data.school_id
        )
        
        # Persist through repository
        return await self.student_repo.create(student)

# 3. 🏗️ INFRASTRUCTURE LAYER - Database implementation
class StudentRepository(StudentRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, student: Student) -> Student:
        # Convert domain to database entity
        entity = StudentMapper.to_entity(student)
        
        # Database operations
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        
        # Convert back to domain
        return StudentMapper.to_domain(entity)

# 4. 🎨 PRESENTATION LAYER - API interface
@router.post("/students/", response_model=StudentResponseDTO)
async def create_student(
    student_data: StudentCreateDTO,
    service: StudentService = Depends(get_student_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new student"""
    student = await service.enroll_student(student_data)
    return StudentResponseDTO.from_domain(student)
```

## 🚀 Quick Start

### Choose Development Environment

This project supports three different development environments:

#### 🏠 **Local Development** (without Docker)
```bash
# Requires local PostgreSQL installation
# Use .env configuration

# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up local environment (optional helper)
python setup_env.py

# 3. Run the application
make local
# OR
uvicorn app.main:app --reload
```

#### 🐳 **Docker Development** 
```bash
# Complete containerized environment
# Use .env.docker configuration

# Start development environment
make dev

# Access the application
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - pgAdmin: http://localhost:5050 (admin@mattilda.com / admin123)

# Test with default admin user
# Login at http://localhost:8000/docs with: admin / admin123
```

#### 🚀 **Docker Production**
```bash
# Production-ready deployment
# Use .env.prod configuration

# 1. Configure production environment
# Edit .env.prod with secure values

# 2. Deploy
make prod
```

## 📊 Features

### Core Entities
- **Schools**: Complete school management with address, contact info, and principal details
- **Students**: Student records with enrollment, grade levels, and contact information  
- **Invoices**: Billing system with payment tracking and status management

### API Capabilities
- **CRUD Operations**: Full Create, Read, Update, Delete for all entities
- **Advanced Filtering**: Filter by any field with partial matching
- **Pagination**: Configurable page size and navigation
- **Validation**: Comprehensive business rule validation
- **Type Safety**: Full type hints and Pydantic models

### Filtering Examples
```bash
# Filter schools by state and city
GET /api/v1/schools/?state=CA&city=Los%20Angeles&page=1&size=10

# Filter students by grade and school
GET /api/v1/students/?grade_level=10&school_id=1&is_active=true

# Filter invoices by status and date range
GET /api/v1/invoices/?status=pending&amount_min=100&amount_max=1000
```

## 🛠️ Development

### Local Development (Docker)
```bash
# Start development environment
make dev

# View logs
make logs-backend

# Run tests
make test

# Open backend shell
make shell

# Open database shell  
make db-shell
```

### Local Development (Native)
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database settings

# Run the application
uvicorn app.main:app --reload

# Run tests
python run_tests.py domain --verbose
```

## 🐘 Database

### Schema
- **schools**: School information and metadata
- **students**: Student records linked to schools
- **invoices**: Billing records linked to students and schools

### Management
```bash
# Access database shell
make db-shell

# Start pgAdmin for GUI management
make pgadmin

# Create backup
make backup

# Restore from backup
make restore BACKUP_FILE=backups/backup_20240101_120000.sql
```

## 🧪 Testing

### Unit Tests (72 total tests)
- **Domain Models**: Complete business logic validation
- **Test Coverage**: 100% coverage of domain layer
- **Test Categories**: Validation, business methods, boundary values

```bash
# Run all domain tests
make test
# OR
python run_tests.py domain --verbose

# Run specific test file
pytest tests/unit/domain/test_school_model.py -v

# Run with coverage
python run_tests.py coverage
```

### 🔐 Testing with Default Admin User

The system automatically creates a default admin user for testing and development:

#### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123` (development), see env files for other environments
- **Email**: `admin@example.com` (development)
- **Role**: Superuser (access to all admin endpoints)

#### Quick Admin Testing

**1. Start the development environment:**
```bash
make dev
```

**2. Login and get access token:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

**3. Test admin endpoints with the token:**
```bash
# Get current user info
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer ACCESS_TOKEN"

# List all users (admin only)
curl -X GET "http://localhost:8000/api/v1/auth/users" \
     -H "Authorization: Bearer ACCESS_TOKEN"

# Cache management (admin only)
curl -X GET "http://localhost:8000/api/v1/cache/stats" \
     -H "Authorization: Bearer ACCESS_TOKEN"
```

#### Using Interactive API Documentation
1. Open http://localhost:8000/docs
2. Click **"Authorize"** button (top right)
3. Login with `admin` / `admin123`
4. Test any endpoint directly in the browser

#### Available Admin Endpoints
| Method | Endpoint | Description | Auth Level |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/auth/users` | List all users | Superuser |
| `GET` | `/api/v1/auth/users/{id}` | Get user by ID | Superuser |
| `GET` | `/api/v1/cache/stats` | Cache statistics | Superuser |
| `DELETE` | `/api/v1/cache/clear` | Clear all caches | Superuser |
| `GET` | `/api/v1/cache/health` | Cache health check | Superuser |

## 🚀 Production Deployment

### 1. Prepare Environment
```bash
# Copy and configure production environment
cp .env.prod.example .env.prod

# Edit .env.prod with secure production values:
# - Strong DATABASE_PASSWORD
# - Secure SECRET_KEY (32+ chars)
# - Proper ALLOWED_ORIGINS
# - Production database settings
```

### 2. Deploy
```bash
# Start production environment
make prod

# OR manually
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### 3. Verify Deployment
```bash
# Check health
curl https://yourdomain.com/health

# Monitor services
make status
make logs
```

## 📖 API Documentation

### Endpoints

#### Schools
- `GET /api/v1/schools/` - List schools with filtering
- `POST /api/v1/schools/` - Create new school
- `GET /api/v1/schools/{id}` - Get school by ID
- `PUT /api/v1/schools/{id}` - Update school
- `DELETE /api/v1/schools/{id}` - Delete school

#### Students  
- `GET /api/v1/students/` - List students with filtering
- `POST /api/v1/students/` - Create new student
- `GET /api/v1/students/{id}` - Get student by ID
- `PUT /api/v1/students/{id}` - Update student
- `DELETE /api/v1/students/{id}` - Delete student

#### Invoices
- `GET /api/v1/invoices/` - List invoices with filtering
- `POST /api/v1/invoices/` - Create new invoice
- `GET /api/v1/invoices/{id}` - Get invoice by ID
- `PUT /api/v1/invoices/{id}` - Update invoice
- `DELETE /api/v1/invoices/{id}` - Delete invoice

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Files

The project uses different environment files for different scenarios:

- **`.env`** - Default environment
- **`.env.docker`** - Docker development environment  
- **`.env.prod`** - Docker production environment

#### Local Development (.env)
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/mattilda_db
ENVIRONMENT=development
DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000
```

#### Docker Development (.env.docker)
```bash
DATABASE_URL=postgresql://mattilda_user:mattilda_password@db:5432/mattilda_db
ENVIRONMENT=development
DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
```

#### Docker Production (.env.prod)
```bash
DATABASE_URL=postgresql://prod_user:SECURE_PASSWORD@db:5432/mattilda_prod
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=VERY_LONG_SECURE_KEY_32_PLUS_CHARACTERS
ALLOWED_ORIGINS=https://yourdomain.com
```

### Environment Variables

#### Database
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_HOST` - Database host
- `DATABASE_PORT` - Database port (default: 5432)
- `DATABASE_NAME` - Database name
- `DATABASE_USER` - Database username
- `DATABASE_PASSWORD` - Database password

#### Application
- `ENVIRONMENT` - Environment mode (development/production)
- `DEBUG` - Debug mode (true/false)
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT token expiration in minutes
- `ALLOWED_ORIGINS` - CORS allowed origins
- `APP_HOST` - Application host (127.0.0.1 for local, 0.0.0.0 for Docker)
- `APP_PORT` - Application port (default: 8000)

#### Default Admin User
- `ADMIN_USERNAME` - Default admin username (default: admin)
- `ADMIN_EMAIL` - Default admin email
- `ADMIN_PASSWORD` - Default admin password
- `ADMIN_FULL_NAME` - Default admin display name

## 📋 Available Commands

### Docker Commands (via Makefile)
```bash
make local       # Run locally without Docker
make dev         # Start Docker development environment
make prod        # Start Docker production environment  
make build       # Build Docker images
make up          # Start services
make down        # Stop services
make restart     # Restart services
make logs        # Show all logs
make logs-backend # Show backend logs
make logs-db     # Show database logs
make clean       # Clean up everything
make test        # Run tests
make shell       # Open backend shell
make db-shell    # Open database shell
make pgadmin     # Start pgAdmin
make status      # Check service status
make backup      # Create database backup
make restore     # Restore database
```

### Environment Commands
```bash
python setup_env.py          # Interactive environment setup
python setup_env.py info     # Show environment information
python setup_env.py check    # Check environment files
python setup_env.py status   # Show current configuration
```

### Test Commands
```bash
python run_tests.py domain    # Run domain tests
python run_tests.py coverage  # Run with coverage
python run_tests.py specific --test-path tests/unit/domain/test_school_model.py
```
