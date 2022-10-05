from AI import PlayerAI
from player import Player
import random
from utils import *

def generate_ship_sizes(nb):
    """Generate the sizes of the ships with a certain repartition

    Args:
        nb (int): number of ship  to create

    Returns:
        list(int): list of ship sizes
    """
    sizes = []
    for x in range(nb):
        r = random.random()
        if r<0.1:
            sizes.append(2)
        elif r<0.2:
            sizes.append(5)
        elif r<0.5:
            sizes.append(4)
        else:
            sizes.append(3)
    return sizes

class Game():
    def __init__(self):
        """Create a new game instance, a game instance handles players rounds and players moves
        """
        
        self.nb_ships = 3
        self.nb_mines = 8
        self.random_placement = True
        
        #init of both players
        self.player1 = None
        self.player2 = None
        self.current_player = self.player1
        self.current_opponent = self.player2
        
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
        self.hint_radius = 2
        
        self.placement_type = "Ship"      

    def switch_placement_type(self):
        self.placement_type = "Ship" if self.placement_type=="Mine" else "Mine"
    
    def start_game(self):
        sizes = generate_ship_sizes(self.nb_ships)
        self.player1 = Player("P1",sizes,self.nb_mines,self.random_placement)
        self.player2 = Player("P2",sizes,self.nb_mines,self.random_placement)
        self.current_player = self.player1
        self.current_opponent = self.player2
    
    def change_ship_nb(self,val):
        self.nb_ships+=val
        if self.nb_ships > MAX_SHIP_NB:
            self.nb_ships=MAX_SHIP_NB
        elif self.nb_ships<MIN_SHIP_NB:
            self.nb_ships=MIN_SHIP_NB
    
    def change_mine_nb(self,val):
        self.nb_mines+=val
        if self.nb_mines > MAX_MINE_NB:
            self.nb_mines=MAX_MINE_NB
        elif self.nb_mines<MIN_MINE_NB:
            self.nb_mines=MIN_MINE_NB

    def switch_random_placement(self):
        self.random_placement = not self.random_placement
    
    def change_hint_radius(self,val):
        self.hint_radius+=val
        if self.hint_radius > MAX_HINT_RADIUS:
            self.hint_radius=MAX_HINT_RADIUS
        elif self.hint_radius<0:
            self.hint_radius=0
    
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
    
    def change_player(self):
        """Update game properties for the next round :
            - swap the role of the players
        """
        self.current_opponent ,self.current_player=self.current_player, self.current_opponent
    
    def find_neighbors(self,idx):
        
        neib = set()
        x,y = get_coords(idx)
        
        for a in range(-self.hint_radius,self.hint_radius+1):
            for b in range((abs(a)-self.hint_radius),-(abs(a)-self.hint_radius)+1):
                if 0<=x+a<NB_TILE and 0<=y+b<NB_TILE and not(a == 0 and b == 0):
                    neib.add(get_index(x+a,y+b))
        
        return neib
                    
    def compute_hint(self,neib):
        """This function scans the squares within a radius of 2 squares around the player's shot 
        and saves the information on the number of ships and mines in this area

        Args:
            idx (int):  index corresponding to the coords of the shot of the player
        """
        nb_m = 0
        nb_s = 0
        for n in neib:
            if n in self.current_opponent.list_tiles_mines:
                nb_m+=1
            elif n in self.current_opponent.list_tiles_ships:
                nb_s+=1
                    
        return nb_m, nb_s
    
    def play(self,x,y):
        played = self.current_player.make_move(x,y,self.current_opponent)
        
        if played:
            idx=get_index(x,y)
            neib = self.find_neighbors(idx)
            nb_m, nb_s = self.compute_hint(neib)
            args = () if type(self.current_player)==PlayerAI else (idx, (nb_s,nb_m))
            self.current_player.add_hint(*args)
        
        return played
        
        
        
        