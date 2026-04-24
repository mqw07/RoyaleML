from inference_sdk import InferenceHTTPClient
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com", 
    api_key=os.getenv("ROBOFLOW_API_KEY") 
)
_ASSETS = Path(__file__).resolve().parent / "Assets"
gameplay_image_url = _ASSETS / "Game_Data" / "gameplay41.png"

def identify(image_path) -> dict:
    # Inference the image using the Roboflow API
    results = CLIENT.infer(str(image_path), model_id="clash-royale-bot-3tpmk/1") 
    prediction_data = (results['predictions'])[0]
    return {'Name': prediction_data['class'], 'Confidence': prediction_data['confidence'], 'Position': (prediction_data['x'], prediction_data['y']), 'Time': prediction_data['time']}

print(identify(gameplay_image_url))

