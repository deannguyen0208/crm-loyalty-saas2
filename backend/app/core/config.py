from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cafe Loyalty SaaS"
    api_prefix: str = "/api"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./cafe_saas.db"
    cors_origins: list[str] = ["http://localhost:5173"]

    # cloud storage placeholders (S3, GCS...)
    cloud_bucket_name: str = "demo-cafe-saas-backups"
    cloud_region: str = "ap-southeast-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
