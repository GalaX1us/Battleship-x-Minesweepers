import random

from AI import PlayerAI
from player import Player
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
        """
        Create a new game instance, a game instance handles players rounds and players moves
        """
        
        self.nb_ships = 3
        self.nb_mines = 8
        self.random_placement = True
        
        #init of both players
        self.player1 = None
        self.player2 = None
        self.current_player = self.player1
        self.current_opponent = self.player2
        
        self.winner = None
        
        #is the game over yet
        self.over = False
        self.rounds = 0
        
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
        
        self.pause = False
    
    def switch_pause(self):
        self.pause = not self.pause

    def switch_placement_type(self):
        """
        Function used to swap placement type
        """
        self.placement_type = "Ship" if self.placement_type=="Mine" else "Mine"
    
    def init_players(self,AI_nb=0):
        """
        initializes the players according to the number of AI

        Args:
            AI (int, optional): number of AI in the game (0,1 or 2). Defaults to 0.
        """
        sizes = generate_ship_sizes(self.nb_ships)
        if AI_nb==0:
            self.player1 = Player("P1",sizes,self.nb_mines,self.random_placement)
            self.player2 = Player("P2",sizes,self.nb_mines,self.random_placement)
        elif AI_nb == 1:
            self.player1 = Player("P1",sizes,self.nb_mines,self.random_placement)
            self.player2 = PlayerAI("AI",sizes,self.nb_mines)
        else:
            self.player1 = PlayerAI("AI(1)",sizes,self.nb_mines)
            self.player2 = PlayerAI("AI(2)",sizes,self.nb_mines)
            
        self.current_player = self.player1
        self.current_opponent = self.player2
    
    def change_ship_nb(self,val):
        """
        Update the number of ship in the game

        Args:
            val (int): increment value
        """
        self.nb_ships+=val
        if self.nb_ships > MAX_SHIP_NB:
            self.nb_ships=MAX_SHIP_NB
        elif self.nb_ships<MIN_SHIP_NB:
            self.nb_ships=MIN_SHIP_NB
    
    def change_mine_nb(self,val):
        """
        Update the number of mine in the game

        Args:
            val (int): increment value
        """
        self.nb_mines+=val
        if self.nb_mines > MAX_MINE_NB:
            self.nb_mines=MAX_MINE_NB
        elif self.nb_mines<MIN_MINE_NB:
            self.nb_mines=MIN_MINE_NB

    def switch_random_placement(self):
        """
        Swap random placement method (True/False)
        """
        self.random_placement = not self.random_placement
    
    def change_hint_radius(self,val):
        """
        Update the radius of the hint in the game

        Args:
            val (int): increment value
        """
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
        """
        Update game properties for the next round :
            - swap the role of the players
        """
        self.current_opponent ,self.current_player=self.current_player, self.current_opponent
    
    def find_neighbors(self,idx):
        """
        Find all the neighbors of a specific tile

        Args:
            idx (idx): indexes whose neighbors must be found

        Returns:
            list(int): list of all neighbors
        """
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
            if n in self.current_opponent.board.list_tiles_mines:
                nb_m+=1
            elif n in self.current_opponent.board.list_tiles_ships:
                nb_s+=1
                    
        return nb_m, nb_s
    
    def play(self,x=0,y=0):
        """
        makes the player play and computes the hints

        Args:
            x (int, optional): horizontal coord. Defaults to 0.
            y (int, optional): vertical coord. Defaults to 0.
        """
        
        if type(self.current_player)==PlayerAI:
            index = self.current_player.make_move(self.current_opponent)
        else:
            self.current_player.make_move(x,y,self.current_opponent)
        
        if self.current_player.has_played:
            
            idx = index if type(self.current_player)==PlayerAI else get_index(x,y)
            neib = self.find_neighbors(idx)
            nb_m, nb_s = self.compute_hint(neib)
            args = (idx, nb_s, nb_m, neib) if type(self.current_player)==PlayerAI else (idx, nb_s, nb_m)
            self.current_player.add_hint(*args)
            
            #trigger the end of the game
            if not self.current_player.is_alive() or not self.current_opponent.is_alive():
                self.over = True
                self.winner = self.current_player if not self.current_opponent.is_alive() else self.current_opponent
    
    def next_round(self):
        """
        Launch the next round
        """
        self.current_player.has_played=False
        self.change_player()
        self.rounds+=1
        self.pause = False
        
        
        
        
        
        