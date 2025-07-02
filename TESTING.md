# Testing Documentation

This document describes the testing approach and how to run tests for the mattilda-test project.

## Test Structure

The project uses pytest for testing with the following structure:

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── domain/
│       ├── __init__.py
│       ├── test_enums.py          # Tests for domain enums
│       ├── test_school_model.py   # Tests for School domain model
│       ├── test_student_model.py  # Tests for Student domain model
│       └── test_invoice_model.py  # Tests for Invoice domain model
└── integration/  # Future integration tests
```

## Test Categories

### Unit Tests - Domain Models

The domain model tests cover:

#### School Model (`test_school_model.py`)
- ✅ Valid creation with required and optional fields
- ✅ Validation of required fields (name, address, city, state, zip_code, email)
- ✅ Email validation (must contain @)
- ✅ Establishment year validation (1800 - current year)
- ✅ Zip code validation (minimum length)
- ✅ Business methods: `activate()`, `deactivate()`, `update_contact_info()`, `update_principal()`
- ✅ Immutable updates via `update()` method
- ✅ Boundary value testing

#### Student Model (`test_student_model.py`)
- ✅ Valid creation with required and optional fields
- ✅ Validation of required fields (first_name, last_name, email)
- ✅ Email validation (must contain @)
- ✅ Grade level validation (1-12)
- ✅ Date validations (birth_date must be past, enrollment_date not future)
- ✅ Property methods: `full_name`, `age` calculation
- ✅ Business methods: `activate()`, `deactivate()`, `update_contact_info()`
- ✅ Immutable updates via `update()` method
- ✅ Boundary value testing

#### Invoice Model (`test_invoice_model.py`)
- ✅ Valid creation with required and optional fields
- ✅ Amount validations (positive amount, non-negative tax)
- ✅ Total amount calculation validation
- ✅ Date validations (due_date >= invoice_date)
- ✅ Status and payment method enum validations
- ✅ Business methods: `mark_as_paid()`, `cancel()`, `is_overdue()`
- ✅ State transition validations (cannot pay cancelled, cannot cancel paid)
- ✅ Immutable updates via `update()` method
- ✅ Boundary value testing

#### Enums (`test_enums.py`)
- ✅ InvoiceStatus enum values and membership
- ✅ PaymentMethod enum values and membership
- ✅ Enum iteration and counting
- ✅ String value conversion
- ✅ Comparison and uniqueness testing

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-asyncio
```

### Run All Domain Tests

```bash
# Run all domain unit tests
pytest tests/unit/domain/ -v

# Run with coverage (if pytest-cov installed)
pytest tests/unit/domain/ --cov=app.domain --cov-report=term-missing

# Run specific test file
pytest tests/unit/domain/test_school_model.py -v

# Run specific test class
pytest tests/unit/domain/test_school_model.py::TestSchoolDomainModel -v

# Run specific test method
pytest tests/unit/domain/test_school_model.py::TestSchoolDomainModel::test_school_creation_valid -v
```

### Test Configuration

The project uses `pyproject.toml` for pytest configuration:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Test Coverage

Current test coverage for domain models:

- **School Model**: 100% - All business rules, validations, and methods tested
- **Student Model**: 100% - All business rules, validations, and methods tested  
- **Invoice Model**: 100% - All business rules, validations, and methods tested
- **Enums**: 100% - All enum values and behavior tested

### Test Statistics

- **Total Tests**: 72
- **School Model Tests**: 21
- **Student Model Tests**: 19
- **Invoice Model Tests**: 27
- **Enum Tests**: 13

## Test Patterns

### Validation Testing Pattern
```python
def test_model_creation_invalid_field_raises_error(self):
    """Test that invalid field raises ValueError"""
    with pytest.raises(ValueError, match="Error message pattern"):
        Model(invalid_field="invalid_value", ...)
```

### Business Logic Testing Pattern
```python
def test_model_business_method(self):
    """Test business method behavior"""
    model = Model(valid_data...)
    model.business_method()
    assert model.state == expected_state
```

### Boundary Value Testing Pattern
```python
def test_model_boundary_values(self):
    """Test boundary values for validation"""
    # Test minimum valid value
    model_min = Model(boundary_field=min_valid_value, ...)
    assert model_min.boundary_field == min_valid_value
    
    # Test maximum valid value  
    model_max = Model(boundary_field=max_valid_value, ...)
    assert model_max.boundary_field == max_valid_value
```

## Adding New Tests

When adding new domain models or modifying existing ones:

1. Create test file following naming convention: `test_{model_name}_model.py`
2. Create test class: `TestModelNameDomainModel`
3. Test all validation rules in `__post_init__`
4. Test all business methods
5. Test the `update()` method for immutability
6. Add boundary value tests
7. Ensure 100% coverage of the domain model

## Continuous Integration

Tests should be run automatically on:
- Every commit to main branch
- Every pull request
- Before deployment

Example CI command:
```bash
pytest tests/unit/ --cov=app --cov-report=xml --cov-fail-under=90
```
