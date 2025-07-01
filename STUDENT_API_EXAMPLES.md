# Student API Filtering Examples

## New Comprehensive Filtering Endpoint

The student endpoints have been refactored to provide powerful filtering capabilities through query parameters.

### Base URL: `GET /students/`

### Available Filters:

- `first_name` - Filter by first name (partial match)
- `last_name` - Filter by last name (partial match)  
- `email` - Filter by email (partial match)
- `phone` - Filter by phone (partial match)
- `date_of_birth` - Filter by exact date of birth (YYYY-MM-DD)
- `grade_level` - Filter by grade level (exact match)
- `school_id` - Filter by school ID (exact match)
- `enrollment_date` - Filter by exact enrollment date (YYYY-MM-DD)
- `address` - Filter by address (partial match)
- `is_active` - Filter by active status (true/false)

### Pagination:
- `page` - Page number (default: 1)
- `size` - Items per page (default: 10, max: 100)

## Example API Calls:

### 1. Get all students (no filters)
```
GET /students/?page=1&size=10
```

### 2. Filter by school
```
GET /students/?school_id=1&page=1&size=10
```

### 3. Filter by grade level
```
GET /students/?grade_level=8&page=1&size=10
```

### 4. Search by name (partial match)
```
GET /students/?first_name=Emma&page=1&size=10
GET /students/?last_name=Johnson&page=1&size=10
```

### 5. Filter by active status
```
GET /students/?is_active=true&page=1&size=10
```

### 6. Complex filtering (multiple parameters)
```
GET /students/?school_id=1&grade_level=8&is_active=true&page=1&size=10
```

### 7. Filter by date of birth
```
GET /students/?date_of_birth=2010-03-15&page=1&size=10
```

### 8. Filter by enrollment date
```
GET /students/?enrollment_date=2023-08-15&page=1&size=10
```

### 9. Search by email (partial match)
```
GET /students/?email=emma&page=1&size=10
```

### 10. Search by address (partial match)
```
GET /students/?address=School%20Street&page=1&size=10
```

## Removed Redundant Endpoints:

The following endpoints have been removed as they are now covered by the main filtering endpoint:

- ❌ `GET /students/school/{school_id}` → Use `GET /students/?school_id={school_id}`
- ❌ `GET /students/grade/{grade_level}` → Use `GET /students/?grade_level={grade_level}`  
- ❌ `GET /students/search/by-name/{name}` → Use `GET /students/?first_name={name}` or `GET /students/?last_name={name}`

## Benefits:

1. **Single Endpoint**: One endpoint handles all filtering needs
2. **Flexible Combinations**: Mix and match any filters
3. **Partial Matching**: Text fields support partial matching for better UX
4. **Type Safety**: All filters are strongly typed
5. **Consistent Pagination**: Same pagination pattern across all queries
6. **Clean URLs**: No redundant endpoints to maintain
7. **Better Performance**: Optimized database queries with proper indexing support

## Response Format:

All endpoints return the same paginated response format:

```json
{
  "items": [
    {
      "id": 1,
      "first_name": "Emma",
      "last_name": "Johnson",
      "email": "emma.johnson@email.com",
      "phone": "(217) 555-1001",
      "date_of_birth": "2010-03-15",
      "grade_level": 8,
      "school_id": 1,
      "enrollment_date": "2023-08-15",
      "address": "456 School Street",
      "is_active": true
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```
