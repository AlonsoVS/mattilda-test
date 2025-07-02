# School API Examples

This document provides examples of how to use the School API endpoints with filtering, pagination, and CRUD operations.

## Available Filters

All filtering is done via query parameters on the main GET endpoint:

- `name` - Filter by school name (partial match, case-insensitive)
- `address` - Filter by address (partial match, case-insensitive)
- `city` - Filter by city (partial match, case-insensitive)
- `state` - Filter by state (partial match, case-insensitive)
- `zip_code` - Filter by zip code (partial match, case-insensitive)
- `phone` - Filter by phone number (partial match, case-insensitive)
- `email` - Filter by email (partial match, case-insensitive)
- `principal` - Filter by principal name (partial match, case-insensitive)
- `is_active` - Filter by active status (exact match: true/false)

## Standard Pagination Parameters

- `page` - Page number (starting from 1, default: 1)
- `size` - Items per page (1-100, default: 10)

## Examples

### 1. Get all schools (with pagination)

```bash
GET /schools/?page=1&size=10
```

### 2. Filter by name

```bash
GET /schools/?name=elementary&page=1&size=10
```

### 3. Filter by city

```bash
GET /schools/?city=Springfield&page=1&size=10
```

### 4. Filter by state

```bash
GET /schools/?state=CA&page=1&size=10
```

### 5. Filter by active status

```bash
GET /schools/?is_active=true&page=1&size=10
```

### 6. Filter by principal

```bash
GET /schools/?principal=Johnson&page=1&size=10
```

### 7. Filter by zip code

```bash
GET /schools/?zip_code=90210&page=1&size=10
```

### 8. Complex filtering (multiple parameters)

```bash
GET /schools/?state=CA&city=Los%20Angeles&is_active=true&page=1&size=10
```

### 9. Filter by address

```bash
GET /schools/?address=Main%20Street&page=1&size=10
```

### 10. Filter by email domain

```bash
GET /schools/?email=school.edu&page=1&size=10
```

## CRUD Operations

### Get specific school by ID

```bash
GET /schools/1
```

### Create a new school

```bash
POST /schools/
Content-Type: application/json

{
  "name": "Springfield Elementary",
  "address": "123 Main Street",
  "city": "Springfield",
  "state": "CA", 
  "zip_code": "90210",
  "phone": "555-0123",
  "email": "admin@springfieldelementary.edu",
  "principal": "John Smith",
  "is_active": true
}
```

### Update a school

```bash
PUT /schools/1
Content-Type: application/json

{
  "name": "Springfield Elementary School",
  "principal": "Jane Doe",
  "phone": "555-0124"
}
```

### Delete a school

```bash
DELETE /schools/1
```

## Response Format

All responses follow a consistent format:

### Paginated List Response

```json
{
  "items": [
    {
      "id": 1,
      "name": "Springfield Elementary",
      "address": "123 Main Street", 
      "city": "Springfield",
      "state": "CA",
      "zip_code": "90210",
      "phone": "555-0123",
      "email": "admin@springfieldelementary.edu",
      "principal": "John Smith",
      "student_count": 245,
      "is_active": true
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Single School Response

```json
{
  "id": 1,
  "name": "Springfield Elementary",
  "address": "123 Main Street",
  "city": "Springfield", 
  "state": "CA",
  "zip_code": "90210",
  "phone": "555-0123",
  "email": "admin@springfieldelementary.edu",
  "principal": "John Smith",
  "student_count": 245,
  "is_active": true
}
```

## Notes

- All string filters use partial matching and are case-insensitive
- The `student_count` field in responses shows the current number of active students enrolled in the school
- Only the `is_active` filter uses exact matching (true/false)
- Combine multiple filters to narrow down results
- All CRUD operations require appropriate authentication (when implemented)
