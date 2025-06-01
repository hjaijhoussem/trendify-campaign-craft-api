import datetime as dt

from sqlalchemy import Column, String, Text, Numeric, Boolean, Table
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID as PyUUID 
from common.schemas import BaseSchema
from db.core import metadata
from db.utils import created_at, updated_at, uuid_pk

PgUUID = UUID(as_uuid=False)
    
products = Table(
    "products",
    metadata,
    uuid_pk(),
    Column("name", String, nullable=False, index=True),
    Column("category", String, nullable=False, index=True),
    Column("description", Text, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column("image_url", String, nullable=True),
    Column("is_trend", Boolean, nullable=False, default=False, server_default="false"),
    Column("keywords", String, nullable=True),
    Column("trending_percentage", Numeric(5, 2), nullable=False, default=0, server_default="0"),
    created_at(),
    updated_at(),
)

class Product(BaseSchema):
    id: PyUUID
    name: str
    category: str
    description: str
    price: float
    image_url: str | None = None
    is_trend: bool = False
    keywords: str | None = None
    trending_percentage: float = 0.0
    created_at: dt.datetime
    updated_at: dt.datetime


