import typing as t
from injector import singleton
from uuid import UUID as PyUUID
from sqlalchemy import insert, select, func, delete, update
from db.core import db
from db.utils import map_result, map_to
from products.models import products, Product
from products.schemas import CreateProduct, ProductResponse, UpdateProduct

@singleton
class ProductRepo:

    @map_result
    async def create_product(self, new_product: CreateProduct) -> Product:
        result = await db.fetch_one(insert(products).values(new_product.dict()).returning(products))
        return result
    
    @map_result
    async def get_product_by_name(self, product_name: str) -> t.Optional[Product]:
        result = await db.fetch_one(select(products).where(products.c.name == product_name))
        return result
    
    @map_result
    async def get_product_by_id(self, product_id: PyUUID) -> t.Optional[Product]:
        result = await db.fetch_one(select(products).where(products.c.id == product_id))
        return result
    
    async def get_all_products(self) -> t.List[ProductResponse]:
        query = select(products).order_by(products.c.created_at.desc())
        results = await db.fetch_all(query)
        return [
            ProductResponse(
                id=row['id'],
                name=row['name'],
                category=row['category'],
                description=row['description'],
                price=float(row['price']),
                image_url=row['image_url'],
                is_trend=row['is_trend'],
                keywords=row['keywords'],
                trending_percentage=float(row['trending_percentage']),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            for row in results
        ]
    
    @map_result
    async def update_product(self, product_id: PyUUID, product_update: UpdateProduct) -> Product:
        # Only update fields that are provided (not None)
        update_data = {k: v for k, v in product_update.dict().items() if v is not None}
        if not update_data:
            # If no fields to update, just return the current product
            return await self.get_product_by_id(product_id)
        
        result = await db.fetch_one(
            update(products)
            .where(products.c.id == product_id)
            .values(**update_data)
            .returning(products)
        )
        return result
    
    async def delete_product_by_id(self, product_id: PyUUID):
        """Delete product by ID"""
        await db.execute(delete(products).where(products.c.id == product_id))
    
    # @map_result
    # async def get_company_by_name(self, company_name: str) -> t.Optional[Company]:
    #     result = await db.fetch_one(select(companies).where(companies.c.name == company_name))
    #     return result
    
    # @map_result
    # async def get_company_by_id(self, company_id: PyUUID) -> t.Optional[Company]:
    #     result = await db.fetch_one(select(companies).where(companies.c.id == company_id))
    #     return result
    
    # async def get_all_companies(self) -> t.List[CompanyResponse]:
    #     query = select(
    #         companies.c.id,
    #         companies.c.name,
    #         companies.c.created_at,
    #         companies.c.updated_at,
    #         func.count(projects.c.id).label('projects_nbr')
    #         ).outerjoin(projects, companies.c.id == projects.c.company_id
    #         ).group_by(companies.c.id)
    #     results = await db.fetch_all(query)
    #     return [
    #         CompanyResponse(
    #             id=row['id'],
    #             name=row['name'],
    #             created_at=row['created_at'],
    #             updated_at=row['updated_at'],
    #             projects_nbr=row['projects_nbr']
    #         )
    #         for row in results
    #     ]
    
    # async def delete_company_by_id(self, company_id: PyUUID):
    #     """Delete user by ID"""
    #     await db.execute(delete(companies).where(companies.c.id == company_id))
