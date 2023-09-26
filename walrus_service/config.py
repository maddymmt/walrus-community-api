import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_PORT = os.getenv("MONGO_DB_PORT", None)
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", None)

SERVER_HOST = os.getenv("SERVER_HOST", None)
SERVER_PORT = os.getenv("SERVER_PORT", None)
