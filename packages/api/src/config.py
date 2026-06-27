from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Quotation System API"
    debug: bool = False

    # IMAP Settings
    imap_host: str = "localhost"
    imap_port: int = 993
    imap_user: str = "user@example.com"
    imap_password: str = "password"
    imap_use_ssl: bool = True
    imap_mailbox: str = "INBOX"

    # S3 / MinIO Settings
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "quotations"
    s3_region: str = "us-east-1"

    # MQ Topics
    mq_url: str = "amqp://guest:guest@localhost:5672/"
    mq_quotation_parse_topic: str = "quotation.parse"
    mq_dead_letter_topic: str = "quotation.dead_letter"

    # Mail Listener Settings
    mail_poll_interval: int = 30  # seconds

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
