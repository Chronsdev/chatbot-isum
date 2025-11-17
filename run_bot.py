import os 
import rasa
from dotenv import load_dotenv
load_dotenv()

port = os.environ.get("PORT", "5005")

model_path = "models"  
endpoints_path = "endpoints.yml"  

rasa.run(model=model_path, endpoints=endpoints_path, enable_api=True, port=port)