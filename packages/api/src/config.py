from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False
    rabbitmq_url: str = "amqp://guest:guest@localhost/"

    # Legacy System Configuration (AC-8)
    legacy_system_url: str = "http://legacy-system.local"
    legacy_api_key: str = "default-key"

    # Database Configuration (TASK-005)
    database_url: str = "sqlite+aiosqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
