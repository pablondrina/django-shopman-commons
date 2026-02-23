# Django Shopman Commons

Shared utilities for the [Shopman suite](https://github.com/pablondrina) of Django apps.

This package provides admin base classes, UI helpers, and formatting utilities used across
**Offerman**, **Stockman**, **Craftsman**, **Guestman**, **Doorman**, and **Omniman**.

## Installation

```bash
pip install django-shopman-commons
```

Add to `INSTALLED_APPS` (required for static files like the autocomplete autofill JS):

```python
INSTALLED_APPS = [
    ...
    "shopman_commons",
    ...
]
```

No models or migrations — this is a utility-only app.

For Unfold admin support:

```bash
pip install django-shopman-commons[unfold]
```

## What's Included

| Module | Provides | Used by |
|--------|----------|---------|
| `shopman_commons.contrib.admin_unfold.base` | `BaseModelAdmin`, `BaseTabularInline`, `BaseStackedInline` | stockman, craftsman, offerman, guestman |
| `shopman_commons.contrib.admin_unfold.badges` | `unfold_badge()`, `unfold_badge_numeric()` | stockman, craftsman, offerman, guestman |
| `shopman_commons.formatting` | `format_quantity()` | stockman, craftsman |
| `shopman_commons.admin.mixins` | `AutofillInlineMixin` | offerman (available for all) |

## Admin Unfold Base Classes

Textarea-aware `ModelAdmin` and inline classes for [django-unfold](https://github.com/unfoldadmin/django-unfold).
Automatically reduce textarea height and constrain width to match other form fields.

```python
from shopman_commons.contrib.admin_unfold.base import (
    BaseModelAdmin,
    BaseTabularInline,
    BaseStackedInline,
)

class ProductAdmin(BaseModelAdmin):
    list_display = ["name", "sku"]

class OrderItemInline(BaseTabularInline):
    model = OrderItem
    extra = 1
```

## Badges

Colored badge helpers for Unfold admin list displays.

```python
from shopman_commons.contrib.admin_unfold.badges import unfold_badge, unfold_badge_numeric

# Status badge (uppercase, small text)
unfold_badge("Active", "green")
unfold_badge("Draft", "blue")
unfold_badge("Cancelled", "red")

# Numeric badge (normal text, no uppercase)
unfold_badge_numeric("42", "blue")
unfold_badge_numeric("0.00", "base")
```

Available colors: `base`, `red`, `green`, `yellow`, `blue`.

## AutofillInlineMixin

Auto-fills inline fields from autocomplete selection data (Select2 cache).

```python
from shopman_commons.admin.mixins import AutofillInlineMixin

class OrderItemInline(AutofillInlineMixin, admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ["product"]
    autofill_fields = {"product": {"unit_price_q": "base_price_q"}}
```

When the user selects a product via autocomplete, `unit_price_q` is filled with
the product's `base_price_q`. Target fields become optional automatically.

Multiple targets per source are supported:

```python
autofill_fields = {
    "product": {
        "unit_price_q": "base_price_q",
        "unit": "default_unit",
    }
}
```

Works with both plain Django admin and Unfold:

```python
# Plain admin
class MyInline(AutofillInlineMixin, admin.TabularInline): ...

# Unfold admin
class MyInline(AutofillInlineMixin, BaseTabularInline): ...
```

**Requires:** the source model's autocomplete must include the mapped keys in its
JSON response (via `serialize_result` or `optgroup_label`).

## Formatting

```python
from shopman_commons.formatting import format_quantity

format_quantity(Decimal("10.5"))      # "10.50"
format_quantity(Decimal("3.14159"), 4) # "3.1416"
format_quantity(None)                  # "-"
```

## Suite Apps

| Package | Description |
|---------|-------------|
| [django-offerman](https://github.com/pablondrina/django-offerman) | Product catalog and pricing |
| [django-stockman](https://github.com/pablondrina/django-stockman) | Inventory management |
| [django-craftsman](https://github.com/pablondrina/django-craftsman) | Production planning |
| [django-guestman](https://github.com/pablondrina/django-guestman) | Customer management |
| [django-doorman](https://github.com/pablondrina/django-doorman) | Phone-first authentication |
| [django-omniman](https://github.com/pablondrina/django-omniman) | Omnichannel order hub |

## Requirements

- Python 3.11+
- Django 5.2+
- django-unfold 0.80+ (optional, for `contrib.admin_unfold`)

## License

MIT
