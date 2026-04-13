from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DISCORD_BOT_TOKEN: str
    DISCORD_VOICE_CHANNEL_ID: str
    BASE_URL: str
    TEST_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
