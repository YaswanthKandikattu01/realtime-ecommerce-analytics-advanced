import os

class Settings:
    PROJECT_NAME: str = "Real-Time E-Commerce Analytics"
    API_V1_STR: str = "/api"
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
    FRONTEND_ORIGINS: list[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

settings = Settings()
