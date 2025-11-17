import os 
import rasa
from dotenv import load_dotenv
load_dotenv()

port = os.environ.get("PORT", "5005")

# Arrancar el servidor con el modelo recién entrenado
rasa.run(enable_api=True, port=port)