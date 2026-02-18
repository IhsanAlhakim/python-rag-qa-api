from dotenv import load_dotenv
from dataclasses import dataclass
import os


load_dotenv()

# dengan dataclass, tidak perlu __init__
@dataclass 
class Config:
    dbUser: str
    dbPass: str
    dbHost: str
    dbPort: str
    dbName: str
    openaiApiBase: str
    opneaiApiKey: str

    
def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variabel '{key}' is not set") # program stop
    return value

def create_config() -> Config:
    return Config(
        dbUser=get_env("DB_USER"),
        dbPass=get_env("DB_PASS"),
        dbHost=get_env("DB_HOST"),
        dbPort=get_env("DB_PORT"),
        dbName=get_env("DB_NAME"),
        openaiApiBase=get_env("OPENAI_API_BASE"),
        opneaiApiKey=get_env("OPENAI_API_KEY"),
    )