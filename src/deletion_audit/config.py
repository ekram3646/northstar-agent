import os

class Settings:
    DATASET_DIR: str = os.getenv("DATASET_DIR", "dataset")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    EVALUATION_DIR: str = os.getenv("EVALUATION_DIR", "evaluation")
    PROMPTS_DIR: str = os.getenv("PROMPTS_DIR", "prompts")
    
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "gemini")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
