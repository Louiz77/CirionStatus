import os
from dotenv import load_dotenv

# Carregamento das variaveis (que requer segurança no arquivo .env localizado na pasta da aplicação)
load_dotenv()

class Config:
    UPLOAD_FOLDER = './data'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    BASE_URL = "https://graph.microsoft.com/v1.0"
    DATA_FOLDER = "./data"
    LOG_FOLDER = "./log"

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
