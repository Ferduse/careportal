from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CarePortal API"
    app_version: str = "0.1.0"
    debug: bool = True

    jwt_secret_key: str = "dev-secret-change-before-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CAREPORTAL_")


settings = Settings()
