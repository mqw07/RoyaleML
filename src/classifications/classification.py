from src.classifications import identification


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

def find_new_troops(identification_1, identification_2) -> str:
    """
    Returns dictionary of new troop classes found.
    """
    new_troops = identification_1.keys() - identification_2.keys()
    if not new_troops or len(new_troops) > 1:
        return 
    return new_troops.pop()

def infer_from_movement(identification_1: dict, identification_2: dict) -> dict:
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
            

def infer_from_elixir(identification_1: dict, identification_2: dict, elixir_1: int, elixir_2: int) -> dict:
    """
    Infer the team of the current cards based on the user's elixir spent from two adjacent captures
    """
    res = {}
    initial_troops = identification_1.keys()
    final_troops = identification_2.keys()
    if elixir_2 < elixir_1:
        return


if __name__ == '__main__':
    pass
    