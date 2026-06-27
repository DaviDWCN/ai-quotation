from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False
    rabbitmq_url: str = "amqp://guest:guest@localhost/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
