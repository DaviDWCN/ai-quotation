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

    # S3 Storage Configuration
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_region: str = "us-east-1"
    s3_bucket: str = "quotations"

    # MQ Topics
    mq_quotation_parse_topic: str = "quotation.parse"
    mq_dead_letter_topic: str = "quotation.dead_letter"

    # Mail Configuration
    mail_poll_interval: int = 60
    mail_max_attachment_size: int = 10 * 1024 * 1024  # 10MB

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

settings = Settings()
