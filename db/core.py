from databases import Database
from sqlalchemy import MetaData

from core import cfg

# SQLAlchemy Metadata instance
metadata = MetaData()

# Database instance
db = Database(
    cfg.SQLALCHEMY_DATABASE_URI,
    min_size=cfg.POSTGRES_MIN_POOL_SIZE,
    max_size=cfg.POSTGRES_MAX_POOL_SIZE,
)