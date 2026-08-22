from .pyauto import place_card

def make_decision(identifications: dict, e_count: int):

    # Make decisions wrt the current game state
    y_danger_threshold = 580 # Y level on ally side past bridge
    right_side_threshold = 2125 # X coordinate that determines which side the opposing troop goes towards

    for troop, positions in identifications.items():
        
        for position in positions:
            for (x, y), classification in position.items():

                if y > y_danger_threshold and classification == 'enemy' and e_count >= 5:
                    if x < right_side_threshold:
                        # Card is on left side
                        place_card(1, (x + 1760, y + 150))
                        return
                    else:
                        place_card(1, (x + 1770, y + 150))
                        return

