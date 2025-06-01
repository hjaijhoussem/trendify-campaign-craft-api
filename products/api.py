import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response
from fastapi_utils.cbv import cbv
from loguru import logger

from common.schemas import APIResponse
from core.injection import on
from products.service import ProductService
from products.models import Product
from products.schemas import CreateProduct, ProductResponse, UpdateProduct
# from auth.dependencies import get_current_admin_user
# from auth.schemas import UserInDB
# from fastapi import Body
# from auth.dependencies import get_current_active_user

PREFIX = "/product"
TAG = "Product"

product_router = APIRouter(prefix=PREFIX, tags=[TAG])

@cbv(product_router)
class ProductRouter:
    _service: ProductService = Depends(on(ProductService))

    @product_router.post("/", response_model=APIResponse[Product], status_code=status.HTTP_201_CREATED)
    async def create_product(self, product: CreateProduct):
        logger.info(f"Creating product {product.name}")
        created_product = await self._service.create_product(product)
        return APIResponse[Product](message=f"Product {created_product.name} created successfully", data=created_product)
    
    @product_router.get("/", response_model=APIResponse[t.List[ProductResponse]], status_code=status.HTTP_200_OK)
    async def get_all_products(self):
        logger.info("Getting all products")
        products = await self._service.get_all_products()
        return APIResponse[t.List[ProductResponse]](message="All products fetched successfully", data=products)
    
    @product_router.get("/{product_id}", response_model=APIResponse[ProductResponse], status_code=status.HTTP_200_OK)
    async def get_product_by_id(self, product_id: UUID):
        logger.info(f"Getting product with ID {product_id}")
        product = await self._service.get_product_by_id(product_id)
        return APIResponse[ProductResponse](message="Product fetched successfully", data=product)
    
    @product_router.put("/{product_id}", response_model=APIResponse[Product], status_code=status.HTTP_200_OK)
    async def update_product(self, product_id: UUID, product_update: UpdateProduct):
        logger.info(f"Updating product with ID {product_id}")
        updated_product = await self._service.update_product(product_id, product_update)
        return APIResponse[Product](message=f"Product {updated_product.name} updated successfully", data=updated_product)
    
    @product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_product_by_id(self, product_id: UUID):
        """Delete a product by ID"""
        logger.info(f"Deleting product with ID {product_id}")
        await self._service.delete_product_by_id(product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
