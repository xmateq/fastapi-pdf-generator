from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"
        