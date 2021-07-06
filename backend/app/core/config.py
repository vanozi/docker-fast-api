from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret
from functools import lru_cache

config = Config(".env")
PROJECT_NAME = "Docker-FastAPI"
VERSION = "1.0.0"
API_PREFIX = "/api"
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

REGISTRATION_TOKEN_LIFETIME = config("REGISTRATION_TOKEN_LIFETIME", cast=int)
ACCESS_TOKEN_LIFETIME = config("ACCESS_TOKEN_LIFETIME", cast=int)
ALGORITHM = config("ALGORITHM", cast=str)
MAIL_SENDER = config("MAIL_SENDER", cast=str)
SMTP_HOST = config("SMTP_HOST", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=int)
BASE_URL_FRONTEND = config("BASE_URL_FRONTEND", cast=str)


