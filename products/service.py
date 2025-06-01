import typing as t
from uuid import UUID as PyUUID
from injector import inject, singleton
from products.repo import ProductRepo
from products.models import Product
from products.schemas import CreateProduct, ProductResponse, UpdateProduct
from products.errors import ProductNameAlreadyExistsError
from common.errors import NotFoundError

@singleton
class ProductService:

    @inject
    def __init__(self, product_repo: ProductRepo):
        self.product_repo = product_repo

    async def create_product(self, product: CreateProduct) -> Product:
        product_name_exists = await self.product_repo.get_product_by_name(product.name)
        if product_name_exists:
            raise ProductNameAlreadyExistsError()
        return await self.product_repo.create_product(product)

    async def get_all_products(self) -> t.List[ProductResponse]:
        return await self.product_repo.get_all_products()
    
    async def get_product_by_id(self, product_id: PyUUID) -> t.Optional[ProductResponse]:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            return None
        # Convert Product to ProductResponse using model_validate
        return ProductResponse.model_validate(product.model_dump())
    
    async def update_product(self, product_id: PyUUID, product_update: UpdateProduct) -> Product:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            error_message = f"Product {product_id} not found"
            raise NotFoundError(message=error_message)
        
        # Check if name is being updated and if it already exists
        if product_update.name and product_update.name != product.name:
            existing_product = await self.product_repo.get_product_by_name(product_update.name)
            if existing_product:
                raise ProductNameAlreadyExistsError()
        
        return await self.product_repo.update_product(product_id, product_update)
    
    async def delete_product_by_id(self, product_id: PyUUID):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            error_message = f"Product {product_id} not found"
            raise NotFoundError(message=error_message)
        await self.product_repo.delete_product_by_id(product_id)
