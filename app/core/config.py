import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class BaseSettings:
    PROJECT_NAME:str = "ESC Simulator"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API to simulate ESC results"
    CHROME_DRIVER_PATH : str = os.getenv("CHROME_DRIVER_PATH")

class DevSettings(BaseSettings):
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",str(5432))
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


class TestSettings(BaseSettings):
    POSTGRES_USER : str = os.getenv("TEST_POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("TEST_POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("TEST_POSTGRES_PORT",str(2345))
    POSTGRES_DB : str = os.getenv("TEST_POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


dev_settings = DevSettings() 
test_settings = TestSettings()