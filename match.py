import card_data
import computer_vision
import time

cards = card_data.load_cards_json(card_data.SAMPLE_JSON)

class Match:
    # An instance of a Clash Royale Match, 
    def __init__(self, game_type: str,  f_cards_played: list, o_cards_played: list, activity: bool = True, f_curr_elixir: int = 6, o_curr_elixir: int = 6):

        if game_type == '1v1':
            self.elixir_rate = 1 / 2.8
        elif game_type == '2v2':
            self.elixir_rate = 1 / 3.6
        else:
            raise ValueError(game_type)
        
        self.f_cards_played = f_cards_played
        self.o_cards_played = o_cards_played
        self.activity = activity
        self.f_curr_elixir = f_curr_elixir
        self.o_curr_elixir = o_curr_elixir
# UNFINISHED


class Troop:
    # Pass in the name of model's prediction
    def __init__(self, name) -> None:
        self.name = card_data.translation[name]
        card_dict = cards[self.name]
        self.elixir_cost = card_dict['elixirCost']
        self.group_card = card_dict['groupCard']

        # HP group -> low, med, high
        

    def det_team(self, f_cards_played: list, o_cards_played: list):
        pass

    
        
