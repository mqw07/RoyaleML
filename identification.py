from inference_sdk import InferenceHTTPClient
import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
load_dotenv()

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com", 
    api_key=os.getenv("ROBOFLOW_API_KEY") 
)
_ASSETS = Path(__file__).resolve().parent / "Assets"
gameplay_image_url = _ASSETS / "Game_Data" / "gameplay41.png"

def identify(image) -> dict:
    # Inference the image using the Roboflow API. Can pass in image path, or nparray.
    if isinstance(image, Path):
        image = str(image)
    elif isinstance(image, np.ndarray):
        pass  # keep as ndarray
    else:
        image = str(image)
    
    results = CLIENT.infer(image, model_id="clash-royale-bot-3tpmk/1")
    prediction_data = results['predictions']
    if prediction_data:
        predictions = {}
        for prediction in prediction_data:
            troop_class = prediction['class']
            if troop_class not in predictions:
                predictions[troop_class] = []
            predictions[troop_class].append(
                {
                    'Confidence': prediction['confidence'],
                    'Position': (prediction['x'], prediction['y'])
                }
            )
        predictions['Time'] = results['time'],
        return predictions
    else:
        return {}

if __name__ == '__main__':
    print(identify(gameplay_image_url))
