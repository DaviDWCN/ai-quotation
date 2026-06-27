from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False

    # IMAP Settings
    imap_host: str = "localhost"
    imap_port: int = 993
    imap_user: str = "test@example.com"
    imap_password: str = "password"
    imap_use_ssl: bool = True

    # MinIO Settings
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "admin"
    minio_secret_key: str = "admin123"
    minio_secure: bool = False
    minio_bucket: str = "quotation-attachments"

    # Mail Listener Settings
    mail_polling_interval: int = 30  # seconds

    # RabbitMQ Settings
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
