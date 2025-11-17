import os 
import rasa
from dotenv import load_dotenv
load_dotenv()

port = os.environ.get("PORT", "5005")

# Entrenar antes de arrancar
os.system("rasa train")

# Arrancar el servidor con el modelo recién entrenado
os.system(f"rasa run --enable-api --port {port}")