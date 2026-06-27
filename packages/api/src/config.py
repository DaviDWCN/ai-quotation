from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False

    # Legacy System Configuration
    LEGACY_SYSTEM_URL: str = "http://legacy-system.local"
    LEGACY_API_KEY: str = "default-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
