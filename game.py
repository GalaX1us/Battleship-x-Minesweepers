from player import Player
from utils import *

class Game():
    def __init__(self):
        """Create a new game instance, a game instance handles players rounds and players moves
        """
        #init of both players
        self.player1 = Player("J1")
        self.player2 = Player("J2")
        self.current_player = self.player1
        self.current_opponent = self.player2
        
        #number of rounds played
        self.rounds = 0
        #is the game over yet
        self.over = False
        
        #Show search grid (True).
        #Show player own grid (False)
        #Search grid is the hidden opponent grid with your shot displayed
        #Player's own grid is he's own grid with opponent's shot displayed 
        self.show_search_grid = True
        
        #Only display ships hint if 0
        #Only display mines hint if 1
        #Display both if 2
        #Display none if 3
        self.hint_option = 0
    
    def game_over(self):
        """set the game to over
        """
        self.over = True    
    
    def switch_grid(self):
        """
        Switch between search grid and player own grid
            - Search grid is the hidden opponent grid with your shot displayed
            - Player's own grid is he's own grid with opponent's shot displayed        
        """
        self.show_search_grid = not self.show_search_grid
    
    def switch_hint(self):
        """
        Switch hint type between :
            - Only display ships hint
            - Only display mines hint
            - Display both
            - Display none
        """
        self.hint_option=(self.hint_option+1)%4
        
    def get_grid_choice(self):
        """Return player's grid choice

        Returns:
            bool: - return True for search grid
                  - return False for player's own grid
        """
        return self.show_search_grid
    
    def get_hint_choice(self):
        """Return player's hint choice

        Returns:
            int: - Only display ships hint if 0
                 - Only display mines hint if 1
                 - Display both if 2
                 - Display none if 3
        """
        return self.hint_option
        
    def check_game(self):
        """Check if the game is over

        Returns:
            bool: True if the game is over False otherwise
        """
        return self.over
    
    def get_current_player(self):
        """Return player currently playing

        Returns:
            Player: player currently playing
        """
        return self.current_player
    
    def get_current_opponent(self):
        """Return current opponent

        Returns:
            Player: return current opponent
        """
        return self.current_opponent
    
    def next_round(self):
        """Update game properties for the next round :
            - increments the number of rounds
            - swap the role of the players
        """
        self.rounds+=1
        self.current_opponent ,self.current_player=self.current_player, self.current_opponent
        
    def compute_hint(self,idx):
        """This function scans the squares within a radius of 2 squares around the player's shot 
        and saves the information on the number of ships and mines in this area

        Args:
            idx (int):  index corresponding to the coords of the shot of the player
        """
        x,y=get_coords(idx)
        nb_m = 0
        nb_s = 0
        for a in range(-2,3):
            for b in range((abs(a)-2),-(abs(a)-2)+1):
                if get_index(x+a,y+b) in self.current_opponent.get_list_tiles_mines():
                    nb_m+=1
                elif get_index(x+a,y+b) in self.current_opponent.get_list_tiles_ships() :
                    nb_s+=1
        self.current_player.add_hint(idx, (nb_s,nb_m))

    def next_move(self,x,y):
        """This function performs the player's move

        Args:
            x (int): horizontal coord of the move
            y (int): vertical coord of the move

        Returns:
            bool:   return False if a move has already been made at this coords and True otherwise
        """
        missed=True
        idx = 10*y+x
        
        if self.current_player.get_shot_fired()[idx]!='U':
            return False
        
        if idx in self.current_opponent.get_list_tiles_mines():
            self.current_player.boom()
            self.current_player.set_shot_fired(idx, 'E')
            missed=False
        
        for ship in self.current_opponent.get_ships():
            if idx in ship.get_occupied_tiles():
                ship.getting_shot(idx)
                self.current_player.set_shot_fired(idx, 'H')
                
                #check if the ship is sunk
                if ship.is_sunk():
                    for i in ship.get_occupied_tiles():
                        self.current_player.set_shot_fired(i, 'S')
                    self.current_opponent.boom()
                missed=False
                break
        
        if missed:
            self.current_player.set_shot_fired(idx, 'M')
            self.compute_hint(idx)
        
        return True
        
        
        
        