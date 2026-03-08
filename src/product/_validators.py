# -----------------------------------------------------------------------------
# _validators.py
# Collection of small, reusable validation helpers for product domain rules.
# These are "pure" functions raising ValidationError instead of mutating state.
# Can be used by ProductCard (entity invariants) and ProductService (scenario checks).
# -----------------------------------------------------------------------------

# from __future__ import annotations enables postponed evaluation of type hints, allowing you to reference classes before they are defined and avoiding circular import issues.
from __future__ import annotations

from decimal import Decimal
from typing import Optional


class ValidationError(ValueError):
    """Domain validation error with descriptive messages."""
    pass

def validate_non_empty(value: str, field_name: str) -> None:
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} must not be empty")

def validate_price_non_negative(price: Decimal, field_name: str) -> None:
    if price is None:
        return
    if price < Decimal("0.00"):
        raise ValidationError(f"{field_name} cannot be negative")

def validate_promo_not_higher_than_base(promo: Optional[Decimal], base: Decimal) -> None:
    if promo is None:
        return
    if promo > base:
        raise ValidationError("promo_price cannot be higher than base_price")

def validate_category(value: str) -> None:
    validate_non_empty(value, "category")

def validate_sku(value: str) -> None:
    validate_non_empty(value, "sku")

def validate_title(value: str) -> None:
    validate_non_empty(value, "title")

def validate_photo_name(value: Optional[str]) -> None:
    if value is None:
        return
    if not str(value).strip():
        raise ValidationError("photo_name must not be empty")