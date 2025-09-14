from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")
    EXA_API_KEY: str = os.getenv("EXA_API_KEY", "")

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]

    # Database
    DATABASE_URL: str = "sqlite:///./competitor_intelligence.db"

    # Application settings
    MAX_COMPETITORS: int = 10
    ANALYSIS_TIMEOUT: int = 300

    class Config:
        env_file = ".env"

settings = Settings()