# RoyaleML

Reactionary Clash Royale bot for a Windows-emulated game window. It watches the board, labels troops as ally or enemy, reads elixir, and places cards in response.

## Key functionality

**Screen capture (MSS + OpenCV)**  
MSS grabs the emulator region each tick. OpenCV converts the frame to BGR, shows live debug windows, and feeds crops into detection.

**Troop detection (Roboflow API)**  
A labelled YOLOv11 instance-segmentation model on Roboflow identifies troop class, confidence, and `(x, y)` position for every unit on screen.

**Elixir detection (template matching + ddddocr)**  
The elixir HUD crop is read first with OpenCV template matching against digit templates. If that fails, ddddocr runs on the same crop.

**Team classification by movement**  
Two adjacent frames are compared. Vertical travel (`dy`) marks a troop as enemy (down the board), ally (up), or still. That is how friendly and opposing units are separated without a dedicated team model.

**Heuristic logic + placement (PyAutoGUI)**  
`make_decision` walks the classified positions and elixir count, then PyAutoGUI clicks a hotbar slot and drops the card on the board (for example, a defensive placement when an enemy crosses a y-threshold).

**Running loop**  
`run_loop` in `src/RoyaleML/computer_vision/capture.py` is the main cycle: capture board + elixir → identify → classify from the previous frame → decide and place → sleep to a ~0.7s interval. Press `q` to stop. Alternate frames are used as the previous snapshot so movement can be measured.

## How to run

The bot is built for **Windows** with Clash Royale running in an emulator (or window) on the same machine. Capture regions and click coordinates are hardcoded to a specific window size and position, so you will likely need to edit them.

1. **Use Python 3.12** (not 3.13+). `inference-sdk` does not support newer versions.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Add a Roboflow API key.** Create a `.env` file in the project root (it is gitignored):

```
ROBOFLOW_API_KEY=your_key_here
```

The key is loaded by `identification.py` and sent to `https://serverless.roboflow.com`.

3. **Line up the game window.** Place the emulator so the board matches the regions in `src/RoyaleML/computer_vision/capture.py` (`capture` for the arena, `capture_elixir` for the elixir digit). If troops or elixir look cropped in the OpenCV windows, change `top` / `left` / `width` / `height`. Card-slot and drop coordinates live in `src/RoyaleML/logic/actions.py`.

4. **Start the loop** from the repo root with the venv active:

```powershell
python src/RoyaleML/main.py
```

You can also run `python -m RoyaleML` from the `src` folder. Two OpenCV windows (`Game` and `Live`) should appear. Press **q** in that window to quit.

5. **Safety.** PyAutoGUI will move the mouse and click. Failsafe is on: slam the cursor into a screen corner to abort. Do not run this on a machine you need for other work at the same time.

Optional: `pytest` runs the unit tests (`pythonpath` is already set to `src` in `pyproject.toml`).

## Sample gameplay (rudimentary)

<img width="1147" height="701" alt="sample" src="https://github.com/user-attachments/assets/4cdf5bcf-e30c-4fdb-a117-695c769605a8" />

## Next steps

- Implement a second troop-classification path that factors in elixir spent, not only movement
- Expand the heuristic game-logic engine with many more board cases
- Write more tests
- Refactor data flow so detections and classifications live in class objects instead of being re-parsed from nested dicts on every pass
