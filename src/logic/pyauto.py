import pyautogui
import time
pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True

def click_location(location: tuple):
    # Clicks on the given location

    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()

left_bridge = (1930, 680)
right_bridge = (2320, 680)
mid_left = (2125, 770)
mid_right = (2140, 770)
left_tower = (1930, 840)
right_tower = (2320, 840)

def click_card_icon(location: int):
    # Clicks on the given card icon
    
    if not 0 < location < 5:
        raise ValueError("Not a valid hotbar slot")
    pyautogui.moveTo(1860 + 140 * location, 1250)
    pyautogui.click()

def place_card(card_slot: int, location: tuple):
    # Places card at slot (card_slot) at x, y coordinates defined by location[0], location[1]
    
    click_card_icon(card_slot)
    time.sleep(pyautogui.PAUSE)
    click_location(location)

if __name__ == '__main__':
    place_card(4, right_bridge)