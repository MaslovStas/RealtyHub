from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment

BASE_DIR = Path(__file__).parent.parent


class BaseSettingsEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DbSettings(BaseSettingsEnv):
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/test.db"
    ECHO_DB: bool = False


class AuthJWT(BaseSettingsEnv):
    SECRET_KEY: str = "9a05f682f66f4474ae3abe10e2e6936cf7cb834bfd604e9f69f3a77d15bad348"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class Cloudinary(BaseSettingsEnv):
    CLOUD_NAME: str = ""
    CLOUD_API_KEY: str = ""
    CLOUD_API_SECRET: str = ""


class Settings(BaseSettingsEnv):
    api_v1_prefix: str = "/api/v1"
    ENVIRONMENT: Environment = Environment.LOCAL

    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    cloudinary: Cloudinary = Cloudinary()


settings = Settings()
