import card_data
import computer_vision
import time

cards = card_data.load_cards_json(card_data.SAMPLE_JSON)

class Troop:
    # Pass in the name of model's prediction, and it's 
    def __init__(self, name, y_cord) -> None:
        self.name = card_data.translation[name]
        card_dict = cards[self.name]
        self.elixir_cost = card_dict['elixirCost']
        self.group_card = card_dict['groupCard']
        self.y_cord = y_cord
        if self.y_cord < 580:
            self.team = 'e'
        else:
            self.team = 'f'
        # HP group -> low, med, high
    
class Match:
    # An instance of a Clash Royale Match, want to keep a hashmap of played cards, if a new one appears, add it to the map and count it's elixir.
    def __init__(self, game_type: str, o_curr_elixir: int = 6):

            if game_type == '1v1':
                self.elixir_rate = 1 / 2.8
            elif game_type == '2v2':
                self.elixir_rate = 1 / 3.6
            else:
                raise ValueError(game_type)
            
            self.cards_played = {}
            self.o_curr_elixir = o_curr_elixir
        
    def play_card(self, troop: Troop):
            pass

    
        
