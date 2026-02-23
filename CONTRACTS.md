# shopman_commons -- Contracts

## Public API

### Exceptions (`shopman_commons.exceptions`)

| Symbol | Purpose |
|--------|---------|
| `BaseError(code, message="", **data)` | Base class for all structured exceptions in the suite. Subclass per app (e.g., `CatalogError(BaseError)`). |
| `BaseError.as_dict() -> dict` | Serialize to `{"code", "message", "data"}`. |

Contract: every app exception inherits from `BaseError` and follows the `(code, message, **data)` signature.

### Monetary (`shopman_commons.monetary`)

All monetary values in the suite are **integers in centavos** (suffix `_q`). These functions are the only sanctioned way to do monetary arithmetic.

| Symbol | Signature | Returns |
|--------|-----------|---------|
| `monetary_mult` | `(qty: Decimal, unit_price_q: int) -> int` | Total in centavos, ROUND_HALF_UP. |
| `monetary_div` | `(total_q: int, divisor: int) -> int` | Result in centavos, ROUND_HALF_UP. Raises `ValueError` if divisor <= 0. |
| `format_money` | `(value_q: int) -> str` | Display string with comma decimal separator (e.g., `1250` -> `"12,50"`). |
| `ONE` | `Decimal("1")` | Rounding quantum constant. |

### Formatting (`shopman_commons.formatting`)

| Symbol | Signature | Returns |
|--------|-----------|---------|
| `format_quantity` | `(value: Decimal, decimal_places: int = 2) -> str` | Formatted number string, or `"-"` if value is `None`. |

### Phone (`shopman_commons.phone`)

| Symbol | Signature | Returns |
|--------|-----------|---------|
| `normalize_phone` | `(value: str, default_region="BR", contact_type=None) -> str` | E.164 phone, lowercased email, or lowercased Instagram handle. Empty string on invalid input. |
| `is_valid_phone` | `(value: str, default_region="BR") -> bool` | Validity check. Gracefully degrades if `phonenumbers` is not installed. |

Handles the Manychat bug (Brazilian numbers missing country code 55).

### Admin Mixins (`shopman_commons.admin.mixins`)

| Symbol | Purpose |
|--------|---------|
| `AutofillInlineMixin` | Mixin for `TabularInline`/`StackedInline`. Auto-fills target fields from Select2 autocomplete data via `autofill_fields` dict. Injects `autocomplete_autofill.js`. |

### Unfold Admin (`shopman_commons.contrib.admin_unfold`)

| Symbol | Purpose |
|--------|---------|
| `base.BaseModelAdmin` | `ModelAdmin` with reduced textarea height (50%) and max-width 42rem. |
| `base.BaseTabularInline` | `TabularInline` with reduced textarea height. |
| `base.BaseStackedInline` | `StackedInline` with reduced textarea height. |
| `badges.unfold_badge(text, color="base")` | Render uppercase status badge. Colors: `base`, `red`, `green`, `yellow`, `blue`. |
| `badges.unfold_badge_numeric(text, color="base")` | Render numeric badge (normal case). Same color palette. |

### App Config (`shopman_commons.apps`)

`ShopmanCommonsConfig` -- registered as `shopman_commons` in `INSTALLED_APPS`. Enables Django static file finders to locate bundled JS.

## Invariants

1. **Monetary rounding is always ROUND_HALF_UP.** No other rounding mode is used anywhere in the suite.
2. **Monetary values are always integers in centavos** (suffix `_q`). `monetary_mult` and `monetary_div` are the only sanctioned arithmetic operations.
3. **Phone normalization output is E.164** for valid phone numbers. Email and Instagram inputs pass through lowercased.
4. **`BaseError.as_dict()`** always returns `{"code": str, "message": str, "data": dict}`.
5. **No models, no migrations.** This package is utility-only. Adding it to `INSTALLED_APPS` only registers static files.
6. **`phonenumbers` is an optional dependency.** Phone functions degrade gracefully (basic length validation) if it is absent.

## What Is NOT This Package's Job

- **No models or migrations.** Domain data lives in each app (stockman, doorman, etc.).
- **No business logic.** Validation rules, workflows, and state machines belong to their respective apps.
- **No Django views, URLs, or serializers.** This package does not handle HTTP.
- **No app-specific error codes.** Each app defines its own `BaseError` subclass and codes.
- **No currency conversion or multi-currency.** All values are assumed to be in a single currency (BRL centavos).
- **No i18n of formatted output.** `format_money` always uses comma as decimal separator; `format_quantity` uses period.

## Integration Points

| Consumer | Depends On | How |
|----------|-----------|-----|
| All apps | `BaseError` | Subclass for app-specific exceptions (`CatalogError`, `StockError`, etc.) |
| All apps with monetary fields | `monetary_mult`, `monetary_div`, `format_money` | Arithmetic on `_q` fields, display formatting |
| doorman, guestman | `normalize_phone`, `is_valid_phone` | Contact normalization (replaces per-app implementations) |
| All admin classes (Unfold) | `BaseModelAdmin`, `BaseTabularInline`, `BaseStackedInline` | Consistent textarea sizing across the admin |
| Admin inlines with autocomplete | `AutofillInlineMixin` | Auto-populate price fields from Select2 data |
| Admin list displays | `unfold_badge`, `unfold_badge_numeric` | Colored status/numeric badges in list views |
| Django static files | `ShopmanCommonsConfig` in `INSTALLED_APPS` | Serves `autocomplete_autofill.js` |
