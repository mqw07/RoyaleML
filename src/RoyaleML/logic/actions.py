from pathlib import Path
import sys
import time

import pyautogui

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True

left_back = (2130, 1100)
right_back = (2140, 1100)
mid_left = (2125, 770)
mid_right = (2140, 770)
left_tower = (1930, 840)
right_tower = (2320, 840)


def click_location(location: tuple):
    """Click the given screen location."""
    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()


def click_card_icon(location: int):
    """Click the given card hotbar slot (1-4)."""
    if not 0 < location < 5:
        raise ValueError("Not a valid hotbar slot")
    pyautogui.moveTo(1860 + 140 * location, 1250)
    pyautogui.click()


def place_card(card_slot: int, location: tuple):
    """Place the card in ``card_slot`` at ``location``."""
    click_card_icon(card_slot)
    time.sleep(pyautogui.PAUSE)
    click_location(location)


if __name__ == "__main__":
    place_card(1, left_back)
    print("Hotbar and board landmarks:")
    print(f"  mid_left={mid_left} mid_right={mid_right}")
    print("Skipping live click. Uncomment place_card(4, right_bridge) to test input.")
    # place_card(4, right_bridge)
