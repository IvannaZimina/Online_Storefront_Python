# -----------------------------------------------------------------------------
# ProductCard.py
# Domain model for a product (single source of truth for product data, etc.).
# Encapsulates product fields (SKU, title, category, prices, photo, sales channel)
# and enforces invariants (e.g., non-empty fields, promo_price <= base_price).
# Offers read-only properties and mutation methods with validation.
# -----------------------------------------------------------------------------

from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional

from ._validators import (
    validate_sku, validate_title, validate_category,
    validate_price_non_negative, validate_promo_not_higher_than_base,validate_photo_name
)

#Enum is a data type that specifies a fixed set of valid values.
class SalesChannel(Enum):
    ONLINE_ONLY = "ONLINE_ONLY"
    ONLINE_AND_OFFLINE = "ONLINE_AND_OFFLINE"

class ProductCard:
    def __init__(
        self,
        sku: str,
        title: str,
        short_description: str,
        category: str,
        base_price: Decimal,
        promo_price: Optional[Decimal],
        photo_name: Optional[str],
        sales_channel: SalesChannel,
        is_active: bool = True,
    ):
        # Basic validation of required fields and price logic.
        validate_sku(sku)
        validate_title(title)
        validate_category(category)
        validate_price_non_negative(base_price, "base_price")
        validate_price_non_negative(promo_price, "promo_price")
        validate_promo_not_higher_than_base(promo_price, base_price)

        #declaration of private attributes
        self._sku = sku
        self._title = title
        self._short_description = short_description
        self._category = category
        self._base_price = base_price
        self._promo_price = promo_price
        self._photo_name = photo_name  # just name, not file
        self._sales_channel = sales_channel
        self._is_active = is_active
        
    # getters (read-only properties)
    @property
    def sku(self) -> str:
        return self._sku

    @property
    def title(self) -> str:
        return self._title

    @property
    def short_description(self) -> str:
        return self._short_description

    @property
    def category(self) -> str:
        return self._category

    @property
    def base_price(self) -> Decimal:
        return self._base_price

    @property
    def promo_price(self) -> Optional[Decimal]:
        return self._promo_price

    @property
    def photo_name(self) -> Optional[str]:
        return self._photo_name

    @property
    def sales_channel(self) -> SalesChannel:
        return self._sales_channel

    @property
    def is_active(self) -> bool:
        return self._is_active

    # computed properties

    """
    Returns the price that should be displayed to the user.
    The result is rounded to two decimal places.
    """
    def display_price(self) -> Decimal:
        if self._promo_price is not None:
            price = self._promo_price
        else:
            price = self._base_price
        return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    
    """
    The method encapsulates the rule that only ONLINE_ONLY and ONLINE_AND_OFFLINE channels allow online purchases.
    """
    def can_buy_online(self) -> bool:
        if self._sales_channel == SalesChannel.ONLINE_ONLY:
            return True
        elif self._sales_channel == SalesChannel.ONLINE_AND_OFFLINE:
            return True
        elif self._sales_channel not in SalesChannel:
            raise ValueError(f"Unexpected sales_channel: {self._sales_channel!r}")
        else:
            return False

    # setters (mutations with validation)
    @title.setter
    def title(self, new_title: str) -> None:
        validate_title(new_title)
        self._title = new_title

    @promo_price.setter
    def promo_price(self, new_promo: Optional[Decimal]) -> None:
        validate_price_non_negative(new_promo, "promo_price")
        validate_promo_not_higher_than_base(new_promo, self._base_price)
        self._promo_price = new_promo

    @photo_name.setter
    def photo_name(self, new_photo_name: Optional[str]) -> None:
        validate_photo_name(new_photo_name)
        self._photo_name = new_photo_name

    # For simplicity - changing the sales channel without complex validation here.
    def deactivate(self) -> None:
        self._is_active = False

    def activate(self) -> None:
        self._is_active = True