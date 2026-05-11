from inference_sdk import InferenceHTTPClient
import pytesseract
import os
import cv2 as cv
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
        #predictions['Time'] = results['time'],
        return predictions
    else:
        return {}

def grab_elixir(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    if isinstance(image, np.ndarray):
        img = image
    else:
        img = cv.imread(str(image))
        if img is None:
            return ""

    if img.ndim == 3:
        # Punch up brightness contrast on HUD glow (helps curved 8/9/7 without grayscale binarize).
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4)).apply(hsv[:, :, 2])
        ocr_img = cv.cvtColor(cv.cvtColor(hsv, cv.COLOR_HSV2BGR), cv.COLOR_BGR2RGB)
    else:
        ocr_img = img

    h, w = ocr_img.shape[:2]
    m = min(h, w)
    if m < 120:
        f = 120 / m
        ocr_img = cv.resize(
            ocr_img, (int(round(w * f)), int(round(h * f))), interpolation=cv.INTER_CUBIC
        )

    base = '--oem 3 -c tessedit_char_whitelist=0123456789'
    digits = ''
    for psm in (7, 8, 10):
        raw = pytesseract.image_to_string(ocr_img, config=f'--psm {psm} ' + base).strip()
        digits = ''.join(c for c in raw if c.isdigit())
        if digits:
            break
    if not digits:
        return ''
    return '10' if '10' in digits else digits[-1]

if __name__ == '__main__':
    #print(identify(gameplay_image_url))
    print(grab_elixir(_ASSETS / "Game_Data" / "image.png"))

