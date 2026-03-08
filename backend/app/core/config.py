from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cafe SaaS"
    database_url: str = "sqlite:///./cafe_saas.db"
    jwt_secret: str = "change-me-in-production"
    ai_provider: str = "rule-based"
    openai_api_key: str | None = None
    cloud_storage_dir: str = "./cloud_backups"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
