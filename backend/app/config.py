"""
Configuration management using Pydantic Settings.

Centralizes all environment variables and configuration.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field

# Disable ChromaDB telemetry globally before any imports
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
os.environ['CHROMA_TELEMETRY'] = 'False'


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Create a .env file in the project root with required values.
    See .env.example for template.
    """
    
    # Gemini API Configuration
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_model_name: str = Field(default="gemini-pro", alias="GEMINI_MODEL_NAME")
    temperature: float = Field(default=0.1, alias="TEMPERATURE", ge=0.0, le=2.0)
    
    # Embedding Configuration
    embedding_model_name: str = Field(
        default="all-MiniLM-L6-v2", 
        alias="EMBEDDING_MODEL_NAME"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
settings = Settings()
