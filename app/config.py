import os
from dotenv import load_dotenv

# Подгружаем переменные из .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_DB = int(os.getenv("REDIS_DB") or 0)

# При желании можете добавить другие переменные:
# SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
# DEBUG_MODE = os.getenv("DEBUG", "False") == "True"
