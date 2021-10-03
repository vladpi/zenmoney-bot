from pydantic import BaseSettings, Field, HttpUrl, SecretStr


class Settings(BaseSettings):
    TG_BOT_TOKEN: SecretStr

    ZENMONEY_KEY: str
    ZENMONEY_SECRET: str

    WEBHOOK_HOST: HttpUrl

    LOG_LEVEL: str = Field(default='INFO')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
