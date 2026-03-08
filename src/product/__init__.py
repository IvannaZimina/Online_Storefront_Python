# src/product/__init__.py
"""
product package — public API for the product domain.

Provides:
- UI models: ProductCard, SalesChannel
- View models: ProductItemBase, ProductItemCatalog, ProductItemCarousel
- Service layer: ProductService, CreateProductInput
- Repository contract and JSON implementation: IProductRepository, ProductRepositoryJson

Internal (not exported): validators, storage, CLI, and other technical utilities.
The __init__.py file makes the folder "importable" and controls what will be visible externally when importing product.
"""

from .version import __version__

# ---- Public re-exports (clean API) ------------------------------------------
from .ProductCard import ProductCard, SalesChannel
from .ProductViewModels import (
    ProductItemBase,
    ProductItemCatalog,
    ProductItemCarousel,
)
from .ProductRepositoryJson import (
    IProductRepository,
    ProductRepositoryJson,
)
from .ProductService import (
    ProductService,
    CreateProductInput,
)

# ---- Auto-build __all__ ------------------------------------------------------
import types as _types

__all__ = ["__version__"]

for _name, _obj in list(globals().items()):
    if _name.startswith("_"):
        continue
    if isinstance(_obj, _types.ModuleType):
        continue
    _mod = getattr(_obj, "__module__", "")
    # Экспортируем только то, что пришло из подмодулей пакета product.*
    if _mod.startswith(__name__ + "."):
        __all__.append(_name)

del _name, _obj, _mod, _types


# ---- Explicit public surface -------------------------------------------------
# __all__ = [
#     "__version__",
#     "ProductCard",
#     "SalesChannel",
#     "ProductItemBase",
#     "ProductItemCatalog",
#     "ProductItemCarousel",
#     "IProductRepository",
#     "ProductRepositoryJson",
#     "ProductService",
#     "CreateProductInput",
# ]

