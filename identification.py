from inference_sdk import InferenceHTTPClient
import os
import cv2 as cv
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
from functools import lru_cache

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

_ELIXIR_DIGITS_DIR = _ASSETS / "Game_Data" / "elixir_digits"
_TEMPLATE_SIZE = (32, 48)  # width, height
_TEMPLATE_MIN_SCORE = 0.58
_VALID_ELIXIR = frozenset(str(i) for i in range(11))


def _read_bgr(image) -> np.ndarray | None:
    if not isinstance(image, np.ndarray):
        image = cv.imread(str(image))
    if image is None:
        return None
    if image.ndim == 2:
        return cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    return image


def _elixir_digit_mask(bgr: np.ndarray) -> np.ndarray:
    """Keep the white digit fill; ignore pink/blue HUD and black outline."""
    mask = cv.inRange(bgr, (175, 175, 175), (255, 255, 255))
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=2)
    mask = cv.dilate(mask, kernel, iterations=1)
    if cv.countNonZero(mask) < 24:
        hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
        fallback = cv.inRange(hsv, (0, 0, 195), (179, 70, 255))
        mask = cv.morphologyEx(fallback, cv.MORPH_CLOSE, kernel, iterations=2)
    return mask


def _glyph_boxes(mask: np.ndarray) -> list[tuple[int, int, int, int]]:
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if w * h < 18:
            continue
        boxes.append((x, y, w, h))
    boxes.sort(key=lambda box: box[0])
    return boxes


def _crop_glyph(mask: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = box
    return mask[y : y + h, x : x + w]


def _normalize_glyph(glyph: np.ndarray) -> np.ndarray:
    tw, th = _TEMPLATE_SIZE
    h, w = glyph.shape[:2]
    scale = min(tw / max(w, 1), th / max(h, 1))
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    resized = cv.resize(glyph, (nw, nh), interpolation=cv.INTER_AREA)
    canvas = np.zeros((th, tw), dtype=np.uint8)
    y0, x0 = (th - nh) // 2, (tw - nw) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = resized
    _, canvas = cv.threshold(canvas, 127, 255, cv.THRESH_BINARY)
    return canvas


def _hole_count(glyph: np.ndarray) -> int:
    norm = _normalize_glyph(glyph)
    contours, hierarchy = cv.findContours(norm, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return 0
    return sum(1 for i in range(len(contours)) if hierarchy[0][i][3] >= 0)


def _glyph_aspect(glyph: np.ndarray) -> float:
    h, w = glyph.shape[:2]
    return w / max(h, 1)


def _glyph_to_png(glyph: np.ndarray) -> bytes:
    h, w = glyph.shape[:2]
    side = max(h, w)
    pad = max(4, side // 4)
    square = np.zeros((side + 2 * pad, side + 2 * pad), dtype=np.uint8)
    y0 = pad + (side - h) // 2
    x0 = pad + (side - w) // 2
    square[y0 : y0 + h, x0 : x0 + w] = glyph
    scale = max(6, int(220 / side))
    big = cv.resize(square, None, fx=scale, fy=scale, interpolation=cv.INTER_NEAREST)
    bgr = cv.cvtColor(big, cv.COLOR_GRAY2BGR)
    ok, encoded = cv.imencode(".png", bgr)
    return encoded.tobytes()


@lru_cache(maxsize=1)
def _elixir_templates() -> dict[str, np.ndarray]:
    templates: dict[str, np.ndarray] = {}
    if not _ELIXIR_DIGITS_DIR.is_dir():
        return templates
    for path in sorted(_ELIXIR_DIGITS_DIR.glob("*.png")):
        label = path.stem
        if label not in _VALID_ELIXIR:
            continue
        raw = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
        if raw is None:
            continue
        templates[label] = _normalize_glyph(raw)
    return templates


@lru_cache(maxsize=1)
def _elixir_ocr():
    import ddddocr

    return ddddocr.DdddOcr(show_ad=False)


def _match_template(glyph: np.ndarray) -> str | None:
    norm = _normalize_glyph(glyph)
    templates = _elixir_templates()
    if not templates:
        return None
    best_label, best_score = None, _TEMPLATE_MIN_SCORE
    for label, template in templates.items():
        if template.shape != norm.shape:
            template = cv.resize(template, (norm.shape[1], norm.shape[0]), interpolation=cv.INTER_AREA)
        score = cv.matchTemplate(norm, template, cv.TM_CCOEFF_NORMED)[0][0]
        if score > best_score:
            best_score, best_label = score, label
    return best_label


def _ocr_glyph(glyph: np.ndarray) -> str:
    text = _elixir_ocr().classification(_glyph_to_png(glyph))
    digits = "".join(c for c in text if c.isdigit())
    if not digits:
        return ""
    if digits.startswith("10") or digits.endswith("10"):
        return "10"
    return digits[-1]


def _apply_shape_fixes(glyph: np.ndarray, digit: str) -> str:
    if not digit:
        return ""
    holes = _hole_count(glyph)
    aspect = _glyph_aspect(glyph)
    if digit == "5" and holes >= 1:
        return "9"
    if digit == "9" and holes == 0:
        return "5"
    if digit == "7" and aspect < 0.42:
        return "1"
    if digit == "1" and aspect > 0.52:
        return "7"
    return digit


def _read_glyph(glyph: np.ndarray) -> str:
    digit = _match_template(glyph)
    if digit is None:
        digit = _ocr_glyph(glyph)
    return _apply_shape_fixes(glyph, digit)


def grab_elixir(image) -> str:
    bgr = _read_bgr(image)
    if bgr is None:
        return ""

    mask = _elixir_digit_mask(bgr)
    boxes = _glyph_boxes(mask)
    if not boxes:
        return ""

    glyphs = [_crop_glyph(mask, box) for box in boxes]
    if len(glyphs) >= 2:
        left, right = _read_glyph(glyphs[0]), _read_glyph(glyphs[-1])
        if left == "1" and right == "0":
            return "10"

    glyph = glyphs[0]
    if len(glyphs) == 1 and _glyph_aspect(glyph) >= 0.9:
        h, w = glyph.shape[:2]
        split = _try_split_ten(glyph)
        if split:
            return split

    return _read_glyph(glyph)


def _try_split_ten(glyph: np.ndarray) -> str | None:
    h, w = glyph.shape[:2]
    mid = w // 2
    left, right = glyph[:, :mid], glyph[:, mid:]
    if cv.countNonZero(left) < 12 or cv.countNonZero(right) < 12:
        return None
    d0, d1 = _read_glyph(left), _read_glyph(right)
    if d0 == "1" and d1 == "0":
        return "10"
    return None

if __name__ == '__main__':
    #print(identify(gameplay_image_url))
    print(grab_elixir(_ASSETS / "Game_Data" / "image.png"))

