from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False

    # Legacy System Integration
    legacy_system_url: str = "http://legacy-system.local"
    legacy_api_key: str = "mock-key"
    use_mock_gateway: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
