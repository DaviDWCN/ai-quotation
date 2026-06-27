from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False

    # Legacy System Configuration (AC-8)
    legacy_system_url: str = "http://legacy-system.local"
    legacy_api_key: str = "default-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
