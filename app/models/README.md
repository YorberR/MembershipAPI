# Models Package Structure

This package contains all the database models and schemas for the application, organized into logical modules for better maintainability and scalability.

## Structure

```
app/models/
├── __init__.py          # Package exports
├── base.py              # Base models and enums
├── associations.py      # Many-to-many relationship models
├── customer.py          # Customer-related models
├── plan.py              # Plan-related models
├── transaction.py       # Transaction-related models
├── invoice.py           # Invoice-related models
└── models.py            # DEPRECATED - kept for backward compatibility
```

## Usage

### Recommended Import Patterns

```python
# Import specific models
from app.models.customer import Customer, CustomerCreate, CustomerUpdate
from app.models.plan import Plan, PlanCreate, PlanUpdate
from app.models.transaction import Transaction, TransactionCreate

# Import from package (recommended for most cases)
from app.models import Customer, Plan, Transaction, Invoice, StatusEnum

# Import all models (use sparingly)
from app.models import *
```

## Model Categories

### Base Models (`base.py`)
- `StatusEnum`: Common status enumeration
- `BaseModel`: Base model with common functionality

### Association Models (`associations.py`)
- `CustomerPlan`: Many-to-many relationship between customers and plans

### Customer Models (`customer.py`)
- `CustomerBase`: Base customer schema
- `CustomerCreate`: Schema for creating customers
- `CustomerUpdate`: Schema for updating customers  
- `Customer`: Database model for customers

### Plan Models (`plan.py`)
- `PlanBase`: Base plan schema
- `PlanCreate`: Schema for creating plans
- `PlanUpdate`: Schema for updating plans
- `Plan`: Database model for plans

### Transaction Models (`transaction.py`)
- `TransactionBase`: Base transaction schema
- `TransactionCreate`: Schema for creating transactions
- `TransactionUpdate`: Schema for updating transactions
- `Transaction`: Database model for transactions

### Invoice Models (`invoice.py`)
- `Invoice`: Pydantic model for invoices with computed totals

## Key Improvements

1. **Separation of Concerns**: Each model type has its own module
2. **Type Safety**: Proper TYPE_CHECKING imports to avoid circular imports
3. **Consistency**: Fixed typo (`ammount` → `amount`)
4. **Documentation**: Added docstrings and field descriptions
5. **Computed Fields**: Used `@computed_field` for calculated properties
6. **Backward Compatibility**: Old imports still work with deprecation warnings

## Migration Guide

If you're updating existing code:

1. Replace imports from `app.models.models` with imports from `app.models`
2. Update any references to `ammount` to use `amount` instead
3. The `Invoice.ammount_total` property is now `amount_total` (backward compatible alias provided)

## Best Practices

- Use specific model imports when you only need a few models
- Use package-level imports for broader usage
- Always use the Create/Update schemas for API endpoints
- Keep the database models (table=True) separate from API schemas