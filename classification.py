def vertical_movement(pos1: tuple, pos2: tuple, min_movement = 3) -> str:
    """
    Determines the movement of a class for two given positions
    """

    dy = pos2[1] - pos1[1]
    if dy > min_movement:
        return 'enemy'
    elif dy < -min_movement:
        return 'ally'
    return 'still'

def infer_team_motion(identification_1: dict, identification_2: dict, elixir_difference: int) -> dict:
    """
    Infer the team of the current cards based off of data collected from 2 adjacent captures
    """
    res = {}
    if not identification_1 or not identification_2:
        return res
    common_troops = identification_1.keys() & identification_2.keys()
    for troop in common_troops:
        res[troop] = []
        for i in range(min(len(identification_1[troop]), len(identification_2[troop]))):
            pos2 = identification_2[troop][i]['Position']
            res[troop].append({pos2 :vertical_movement(identification_1[troop][i]['Position'], pos2)})
    return res
            
if __name__ == '__main__':
    pass
    