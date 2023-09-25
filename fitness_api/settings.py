from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_connection_string: str = "sqlite:///./test.db"
    debug_logging: bool = False
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_prefix = "FITNESS_API_"
        env_file_encoding = "utf-8"
        case_sensitive = False


SETTINGS = Settings()
