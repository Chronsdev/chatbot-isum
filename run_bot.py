import os 
from dotenv import load_dotenv
load_dotenv()

port = os.environ.get("PORT", "5005")
os.system(f"rasa run --enable-api --port {port}")