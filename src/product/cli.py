# -----------------------------------------------------------------------------
# cli.py
# Tiny demonstration script for manually exercising the product module.
# Creates a repository + service, inserts a couple of products, and prints
# catalog items. Helpful for quick manual checks without a full UI or tests.

#Command to run:
# python -m product.cli
# -----------------------------------------------------------------------------

from decimal import Decimal, getcontext
from pathlib import Path
from src.product.ProductCard import SalesChannel
from src.product.ProductRepositoryJson import ProductRepositoryJson
from src.product.ProductService import ProductService, CreateProductInput


def run_demo():
    getcontext().prec = 28

    storage_dir = Path(__file__).parent / "product" / "storage"
    repo = ProductRepositoryJson(storage_dir / "products.json")
    photos_dir = storage_dir / "photos"
    service = ProductService(repo, photos_dir)

    # Created Products
    for payload in [
        CreateProductInput(
            sku="SKU001",
            title="USB-C кабель 1м",
            short_description="Lorem ipsum dolor sit amet.",
            category="Кабели",
            base_price=Decimal("9.99"),
            promo_price=Decimal("7.99"),
            photo_name="usb_c_cable.jpg",
            sales_channel=SalesChannel.ONLINE_AND_OFFLINE,
        ),
        CreateProductInput(
            sku="SKU002",
            title="E-book 'OOP Basics'",
            short_description="Учебник по ООП.",
            category="Книги",
            base_price=Decimal("12.00"),
            promo_price=None,
            photo_name="ebook_cover.png",
            sales_channel=SalesChannel.ONLINE_ONLY,
        ),
    ]:
        try:
            service.create(payload)
        except ValueError:
            pass

    # Catalog
    print("Catalog:")
    for item in service.list_catalog_items():
        print(f"- {item.sku}: {item.title} — {item.display_price}€ [{item.category}]")

    # Updates
    updated = service.update_promo_price("SKU001", Decimal("6.99"))
    print(f"\nSale: {updated.sku} is now {updated.display_price()}€")

    # Deactivation
    deactivated = service.deactivate("SKU002")
    print(f"Deactivated: {deactivated.sku} (active={deactivated.is_active})")

    print("\nCatalog after changes:")
    for item in service.list_catalog_items():
        print(f"- {item.sku}: {item.title} — {item.display_price}€ [{item.category}]")


if __name__ == "__main__":
    run_demo()