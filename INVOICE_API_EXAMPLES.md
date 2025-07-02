# Invoice API Filtering Examples

## New Comprehensive Filtering Endpoint

The invoice endpoints have been refactored to provide powerful filtering capabilities through query parameters with support for range filtering and text search.

### Base URL: `GET /invoices/`

### Available Filters:

#### Basic Filters:
- `invoice_number` - Filter by invoice number (partial match)
- `student_id` - Filter by student ID (exact match)
- `school_id` - Filter by school ID (exact match)
- `description` - Filter by description (partial match)
- `status` - Filter by invoice status (PENDING, PAID, OVERDUE, CANCELLED)
- `payment_method` - Filter by payment method (CREDIT_CARD, DEBIT_CARD, BANK_TRANSFER, CASH, CHECK)

#### Amount Range Filters:
- `amount_min` - Filter by minimum amount
- `amount_max` - Filter by maximum amount
- `tax_amount_min` - Filter by minimum tax amount
- `tax_amount_max` - Filter by maximum tax amount
- `total_amount_min` - Filter by minimum total amount
- `total_amount_max` - Filter by maximum total amount

#### Date Range Filters:
- `invoice_date_from` - Filter by invoice date from (YYYY-MM-DD)
- `invoice_date_to` - Filter by invoice date to (YYYY-MM-DD)
- `due_date_from` - Filter by due date from (YYYY-MM-DD)
- `due_date_to` - Filter by due date to (YYYY-MM-DD)
- `payment_date_from` - Filter by payment date from (YYYY-MM-DD)
- `payment_date_to` - Filter by payment date to (YYYY-MM-DD)

### Pagination:
- `page` - Page number (default: 1)
- `size` - Items per page (default: 10, max: 100)

## Example API Calls:

### 1. Get all invoices (no filters)
```
GET /invoices/?page=1&size=10
```

### 2. Filter by student
```
GET /invoices/?student_id=1&page=1&size=10
```

### 3. Filter by school
```
GET /invoices/?school_id=1&page=1&size=10
```

### 4. Filter by status
```
GET /invoices/?status=PENDING&page=1&size=10
GET /invoices/?status=PAID&page=1&size=10
```

### 5. Filter by payment method
```
GET /invoices/?payment_method=CREDIT_CARD&page=1&size=10
```

### 6. Search by invoice number (partial match)
```
GET /invoices/?invoice_number=INV-2024&page=1&size=10
```

### 7. Search by description (partial match)
```
GET /invoices/?description=tuition&page=1&size=10
```

### 8. Amount range filtering
```
GET /invoices/?amount_min=100&amount_max=500&page=1&size=10
GET /invoices/?total_amount_min=1000&page=1&size=10
```

### 9. Date range filtering
```
# Invoices from January 2024
GET /invoices/?invoice_date_from=2024-01-01&invoice_date_to=2024-01-31&page=1&size=10

# Invoices due this month
GET /invoices/?due_date_from=2024-07-01&due_date_to=2024-07-31&page=1&size=10

# Payments made in June 2024
GET /invoices/?payment_date_from=2024-06-01&payment_date_to=2024-06-30&page=1&size=10
```

### 10. Complex filtering (multiple parameters)
```
GET /invoices/?school_id=1&status=PENDING&amount_min=100&due_date_to=2024-07-31&page=1&size=10
```

### 11. Overdue invoices
```
GET /invoices/?status=OVERDUE&page=1&size=10
```

### 12. High-value invoices
```
GET /invoices/?total_amount_min=1000&page=1&size=10
```

## Removed Redundant Endpoints:

The following endpoints have been removed as they are now covered by the main filtering endpoint:

- ❌ `GET /invoices/student/{student_id}` → Use `GET /invoices/?student_id={student_id}`
- ❌ `GET /invoices/school/{school_id}` → Use `GET /invoices/?school_id={school_id}`  
- ❌ `GET /invoices/status/{status}` → Use `GET /invoices/?status={status}`

## Benefits:

1. **Single Endpoint**: One endpoint handles all filtering needs
2. **Range Filtering**: Powerful range filtering for amounts and dates
3. **Flexible Combinations**: Mix and match any filters for complex queries
4. **Text Search**: Partial matching for text fields (invoice_number, description)
5. **Type Safety**: All filters are strongly typed with enum validation
6. **Date Range Support**: Filter by date ranges for better business reporting
7. **Amount Filtering**: Filter by amount ranges for financial analysis
8. **Clean URLs**: No redundant endpoints to maintain
9. **Better Performance**: Optimized database queries with proper indexing support

## Advanced Use Cases:

### Financial Reports:
```
# All paid invoices for Q1 2024 above $500
GET /invoices/?status=PAID&payment_date_from=2024-01-01&payment_date_to=2024-03-31&total_amount_min=500

# Overdue invoices above $100
GET /invoices/?status=OVERDUE&total_amount_min=100

# School-specific revenue for a period
GET /invoices/?school_id=1&status=PAID&payment_date_from=2024-01-01&payment_date_to=2024-06-30
```

### Administrative Tasks:
```
# Invoices due soon
GET /invoices/?status=PENDING&due_date_from=2024-07-01&due_date_to=2024-07-07

# Large unpaid invoices
GET /invoices/?status=PENDING&total_amount_min=1000

# Student payment history
GET /invoices/?student_id=123&status=PAID&payment_date_from=2024-01-01
```

## Response Format:

All endpoints return the same paginated response format:

```json
{
  "items": [
    {
      "id": 1,
      "invoice_number": "INV-2024-001",
      "student_id": 1,
      "school_id": 1,
      "amount": 1000.00,
      "tax_amount": 80.00,
      "total_amount": 1080.00,
      "description": "Tuition Fee - Spring 2024",
      "invoice_date": "2024-01-15",
      "due_date": "2024-02-15",
      "payment_date": "2024-02-10",
      "status": "PAID",
      "payment_method": "CREDIT_CARD",
      "notes": "Paid online",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-02-10T14:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "size": 10,
  "pages": 15
}
```

## Enum Values:

### InvoiceStatus:
- `PENDING`
- `PAID`
- `OVERDUE`
- `CANCELLED`

### PaymentMethod:
- `CREDIT_CARD`
- `DEBIT_CARD`
- `BANK_TRANSFER`
- `CASH`
- `CHECK`
