from ship import *
from mine import *
from utils import *

class Player():
    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8,r_placement=True):     
        
        self.name = name
        self.max_hp = len(ship_sizes)
        self.hp = self.max_hp
        
        self.ships_to_be_placed = ship_sizes
        self.mines_to_be_placed = mine_nb
        
        self.ships = set()
        self.list_tiles_ships = set()
        
        self.mines = set()
        self.list_tiles_mines = set()
        
        #list containing all the moves made by the player
        self.moves_made = [Move.UNKNOWN for i in range(100)]
        self.moves_made_indexes = set()
        
        #list of hint for each move made by the player
        self.hint_list = {}

        self.ready = False
        self.has_played = False
        
        if r_placement:
            #automatic placement of all ships
            self.auto_place_ships(self.ships_to_be_placed)
            #automatic placement of all mines
            self.auto_place_mines(nb=self.mines_to_be_placed)
            self.check_ready()
    
    
    def check_ready(self):
        """
        makes the player ready if he placed all his ships and mines
        """
        if len(self.ships)==len(self.ships_to_be_placed) and len(self.mines) == self.mines_to_be_placed:
            self.ready=True
    
    def place_ship(self,size,coords,orient):
        """
        Check if a ship can be placed at the specified place and if yes, place it

        Args:
            size (int): size of the ship
            coords (tuple(int)): coords of endpoint
            orient (string): orientation
        """
        ship = Ship(size,coords,orient)
        if ship.check_validity(self.list_tiles_ships,self.list_tiles_mines):
            self.ships.add(ship)
            self.list_tiles_ships.update(ship.occupied_tiles)
            self.check_ready()
    
    def place_mine(self,coords):
        """
        Check if a mine can be placed at the specified place and if yes, place it   
        Args:
            coords (tuple(int,int)): coords of the mine
        """
        mine = Mine(coords)
        if mine.check_validity(self.list_tiles_mines,self.list_tiles_ships):
            self.mines.add(mine)
            self.list_tiles_mines.add(mine.get_index())
            self.check_ready()
            
    def auto_place_ships(self, sizes=[3,3,3]):
        """Randomly places all the ships
        
        Args:
            sizes (list(int), optional): ship size list. Defaults to [3,3,3].
        """
        for s in sizes:
            
            #creation of the ship
            ship = Ship(size=s)
            
            #while the ship is invalid create another one
            while not ship.check_validity(self.list_tiles_ships,self.list_tiles_mines):
                ship = Ship(size=s)
            
            #add the newly created ship to the player's ship list
            self.ships.add(ship)
            self.list_tiles_ships.update(ship.occupied_tiles)
            
    def auto_place_mines(self,nb=8):
        """Randomly places all the mines
        
        Args:
            nb (int, optional): number of mines. Defaults 8.
        """
        for x in range(nb):
            mine = Mine()
            while not mine.check_validity(self.list_tiles_mines,self.list_tiles_ships):
                mine = Mine()
                
            self.mines.add(mine)
            self.list_tiles_mines.add(mine.index)      
    
    def add_hint(self,idx,nb_s,nb_m, neib):
        self.hint_list[idx]=(nb_s,nb_m, neib)
    
    def add_move(self,idx,value):
        """Update the list of moves made by player 
        
        Args:
            idx (inx): index of the move
            value (char): type of the move
        """
        self.moves_made[idx]=value
        self.moves_made_indexes.add(idx)
    
    def get_hp_color(self):
        """Returns player's hp and the color corresponding to this value :
            Green if hp > 2/3 max HP
            Orange if 2/3 max hp >= hp > 1/3 max hp
            Red if hp <= 1/3 max hp
        
        Returns:
            tuple(int,tuple(int,int,int)): (player's hp, color)
        """
        color=GREEN
        if self.hp<=(2/3)*self.max_hp:
            color=ORANGE
        if self.hp<=(1/3)*self.max_hp:
            color=RED
        return color
    
    def is_alive(self):
        """Says if the player is still alive
        
        Returns:
            bool: True if player's hp > 0
        """
        return self.hp>0
    
    def boom(self):
        """Removes one HP from the player
        """
        self.hp=max(0, self.hp-1)
        
    def make_move(self,x,y,opponent):
        """This function performs the player's move

        Args:
            x (int): horizontal coord of the move
            y (int): vertical coord of the move

        Returns:
            bool:   return False if a move has already been made at this coords and True otherwise
        """
        missed=True
        idx = 10*y+x
        
        if self.moves_made[idx] is not Move.UNKNOWN:
            return
        
        if idx in opponent.list_tiles_mines:
            self.boom()
            self.add_move(idx, Move.EXPLOSION)
            missed=False
        
        for ship in opponent.ships:
            if idx in ship.occupied_tiles:
                ship.getting_shot(idx)
                self.add_move(idx, Move.HIT)
                
                #check if the ship is sunk
                if ship.sunk:
                    for i in ship.occupied_tiles:
                        self.add_move(i, Move.SUNK)
                    opponent.boom()
                missed=False
                break
        
        if missed:
            self.add_move(idx, Move.MISS)
            
        self.has_played=True
    
