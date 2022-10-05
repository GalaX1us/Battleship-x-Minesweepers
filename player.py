from ship import *
from mine import *
from utils import *

class Player():
    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8,r_placement=True):
        #player's name
        self.name = name
        #max hp value
        self.max_hp = len(ship_sizes)
        #player's hp value 
        self.hp = self.max_hp
        #list of all the player's ships 
        self.ships_to_be_placed = ship_sizes
        self.ships = []
        #list of all index of the tiles occupied by the player's ships
        self.list_tiles_ships = []
        #list of all the player's mines
        self.mines_to_be_placed = mine_nb
        self.mines = []
        #list of all index of the tiles occupied by a player's mines
        self.list_tiles_mines = []
        #list containing all the moves made by the player
        self.moves_made = ['U' for i in range(100)]
        #list of hint for each move made by the player
        self.hint_list = {}
        
        self.ready = False
        
        
        if r_placement:
            #automatic placement of all ships
            self.auto_place_ships(self.ships_to_be_placed)
            #automatic placement of all mines
            self.auto_place_mines(nb=self.mines_to_be_placed)
            self.check_ready()
    
    
    def check_ready(self):
        if len(self.ships)==len(self.ships_to_be_placed) and len(self.mines) == self.mines_to_be_placed:
            self.ready=True
    
    def place_ship(self,size,coords,orient):
        ship = Ship(size,coords,orient)
        if ship.check_validity(self.list_tiles_ships,self.list_tiles_mines):
            self.ships.append(ship)
            self.list_tiles_ships.extend(ship.occupied_tiles)
            self.check_ready()
    
    def place_mine(self,coords):
        mine = Mine(coords)
        if mine.check_validity(self.list_tiles_mines,self.list_tiles_ships):
            self.mines.append(mine)
            self.list_tiles_mines.append(mine.get_index())
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
            self.ships.append(ship)
            self.list_tiles_ships.extend(ship.occupied_tiles)
            
    def auto_place_mines(self,nb=8):
        """Randomly places all the mines
        
        Args:
            nb (int, optional): number of mines. Defaults 8.
        """
        for x in range(nb):
            mine = Mine()
            while not mine.check_validity(self.list_tiles_mines,self.list_tiles_ships):
                mine = Mine()
                
            self.mines.append(mine)
            self.list_tiles_mines.append(mine.index)
    
    def add_hint(self,idx,value):
        """Add an hint to the hint list

        Args:
            idx (int): index of the tile
            value (tuple(int,int)): hints about ships and mines 
        """
        self.hint_list[idx]=value        
    
    
    def add_move(self,idx,value):
        """Update the list of moves made by player 
        
        Args:
            idx (inx): index of the move
            value (char): type of the move
        """
        self.moves_made[idx]=value
    
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
            bool: True if player's hp < 0
        """
        return self.hp>0
    
    def boom(self):
        """Removes one HP from the player
        """
        self.hp=max(0, self.hp-1)
    
    
