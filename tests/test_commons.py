"""
H24 — Commons tests.

Tests for:
- format_quantity() edge cases
- unfold_badge() XSS safety
- AutofillInlineMixin with special characters
"""

from decimal import Decimal

import pytest

from commons.formatting import format_quantity


# ═══════════════════════════════════════════════════════════════════
# format_quantity() tests
# ═══════════════════════════════════════════════════════════════════


class TestFormatQuantity:
    """format_quantity() with edge cases."""

    def test_none_returns_dash(self):
        """None value returns '-'."""
        assert format_quantity(None) == "-"

    def test_zero(self):
        """Zero value formats correctly."""
        assert format_quantity(Decimal("0")) == "0.00"

    def test_negative(self):
        """Negative value formats correctly."""
        assert format_quantity(Decimal("-5.5")) == "-5.50"

    def test_many_decimals_truncates(self):
        """Value with many decimal places is truncated to decimal_places."""
        assert format_quantity(Decimal("1.23456789"), decimal_places=2) == "1.23"

    def test_many_decimals_with_custom_places(self):
        """Custom decimal_places works correctly."""
        assert format_quantity(Decimal("1.23456789"), decimal_places=4) == "1.2346"

    def test_zero_decimal_places(self):
        """decimal_places=0 formats as integer."""
        assert format_quantity(Decimal("10.75"), decimal_places=0) == "11"

    def test_large_number(self):
        """Large numbers format correctly."""
        assert format_quantity(Decimal("999999.99")) == "999999.99"

    def test_very_small_number(self):
        """Very small numbers format correctly."""
        assert format_quantity(Decimal("0.001"), decimal_places=3) == "0.001"

    def test_integer_decimal(self):
        """Integer-like Decimal formats with decimal places."""
        assert format_quantity(Decimal("10")) == "10.00"

    def test_three_decimal_places(self):
        """Three decimal places for weight/volume quantities."""
        assert format_quantity(Decimal("1.955"), decimal_places=3) == "1.955"


# ═══════════════════════════════════════════════════════════════════
# unfold_badge() tests
# ═══════════════════════════════════════════════════════════════════


class TestUnfoldBadge:
    """unfold_badge() XSS safety and behavior."""

    def test_basic_badge(self):
        """Basic badge renders correctly."""
        from commons.contrib.admin_unfold.badges import unfold_badge

        result = unfold_badge("Active", "green")
        assert "Active" in str(result)
        assert "green" in str(result)

    def test_html_in_text_is_escaped(self):
        """HTML in text must be escaped (XSS prevention)."""
        from commons.contrib.admin_unfold.badges import unfold_badge

        result = str(unfold_badge('<script>alert("xss")</script>'))
        # format_html escapes the content
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_html_in_text_with_angle_brackets(self):
        """Angle brackets in text must be escaped."""
        from commons.contrib.admin_unfold.badges import unfold_badge

        result = str(unfold_badge("test<br>break"))
        assert "<br>" not in result
        assert "&lt;br&gt;" in result

    def test_unknown_color_uses_base(self):
        """Unknown color falls back to 'base' styling."""
        from commons.contrib.admin_unfold.badges import unfold_badge

        result = str(unfold_badge("Test", "nonexistent_color"))
        assert "bg-base-100" in result

    def test_badge_numeric(self):
        """unfold_badge_numeric renders without uppercase."""
        from commons.contrib.admin_unfold.badges import unfold_badge_numeric

        result = str(unfold_badge_numeric("42", "blue"))
        assert "42" in result
        assert "uppercase" not in result

    def test_badge_numeric_xss(self):
        """unfold_badge_numeric also escapes HTML."""
        from commons.contrib.admin_unfold.badges import unfold_badge_numeric

        result = str(unfold_badge_numeric('<img src=x onerror="alert(1)">'))
        assert "<img" not in result
        assert "&lt;img" in result


# ═══════════════════════════════════════════════════════════════════
# AutofillInlineMixin tests
# ═══════════════════════════════════════════════════════════════════


class TestAutofillInlineMixin:
    """AutofillInlineMixin with special characters in mapping."""

    def test_mixin_has_autofill_fields_default(self):
        """Default autofill_fields is empty dict."""
        from commons.admin.mixins import AutofillInlineMixin

        assert AutofillInlineMixin.autofill_fields == {}

    def test_mapping_with_special_characters(self):
        """Mapping keys with special characters are serialized safely."""
        import json

        mapping = {"unit_price_q": "base_price_q", "desc": 'value "with" quotes'}
        serialized = json.dumps(mapping)
        parsed = json.loads(serialized)
        assert parsed["desc"] == 'value "with" quotes'

    def test_mapping_with_unicode(self):
        """Mapping with unicode characters serializes correctly."""
        import json

        mapping = {"descricao": "descricao_completa", "preco": "preco_unitario"}
        serialized = json.dumps(mapping, ensure_ascii=False)
        parsed = json.loads(serialized)
        assert parsed["descricao"] == "descricao_completa"

    def test_empty_mapping_no_js_injection(self):
        """Empty mapping doesn't inject JavaScript."""
        from commons.admin.mixins import AutofillInlineMixin

        mixin = AutofillInlineMixin()
        assert not mixin.autofill_fields
