*** IN PROGRESS ***
Reactionary Clash Royale bot that makes decisions based off of:
- Opponent and friendly troop positions
- Elixir counts of opponent/self
- Works through emulated Clash Royale instance on Windows

Troop Classification Model:
- Labelled dataset from Roboflow
- Uses YOLOv11 instance segmentation (multiple troops) and deployed with Roboflow API (Change to Google Colab in the future)
- Identifies class name and quantity of a class on screen

Elixir Counting:
- Utilizes Pytesseract OCR on a cutout of screen to identify self elixir
- Uses this, with a current_troops dictionary to differentiate and track opposing and friendly troops

Computer Vision:
- Running loop of screen to capture the emulated game using MSS and OpenCV
- Feeds current screen instance to Pytesseract and Roboflow for complete current metadata

TODO:
- Implement decision making capabilities and automated playing function with PyAutoGUI
