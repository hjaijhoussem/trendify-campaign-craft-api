from typing import List, Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from common.enums import LogLevelEnum
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")
    PROJECT_NAME: str = "Hack-API"
    API_PREFIX_STR: str = "/api"
    API_VERSION: str
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.DEBUG
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []

    SQLALCHEMY_DATABASE_URI: str
    POSTGRES_MIN_POOL_SIZE: int = 5
    POSTGRES_MAX_POOL_SIZE: int = 10

    # # Authentication settings
    # SECRET_KEY: str = "hippo-zeus-secret-key"
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # # Default admin credentials (can be overridden by environment variables)
    # DEFAULT_ADMIN_USERNAME: str = "admin"
    # DEFAULT_ADMIN_PASSWORD: str = "admin123!"
    
    # # Admin credentials from environment (optional)
    # ADMIN_USERNAME: Optional[str] = None
    # ADMIN_PASSWORD: Optional[str] = None

    # @property
    # def admin_username(self) -> str:
    #     """Get admin username from env or use default"""
    #     return self.ADMIN_USERNAME or self.DEFAULT_ADMIN_USERNAME
    
    # @property
    # def admin_password(self) -> str:
    #     """Get admin password from env or use default"""
    #     return self.ADMIN_PASSWORD or self.DEFAULT_ADMIN_PASSWORD
    

cfg = Settings()