from ship import *
from mine import *
from utils import *

class Player():
    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8):
        #player's name
        self.name = name
        #max hp value
        self.max_hp = 3
        #player's hp value 
        self.hp = self.max_hp
        #list of all the player's ships 
        self.ships = []
        #list of all index of the tiles occupied by the player's ships
        self.list_tiles_ships = []
        #list of all the player's mines
        self.mines = []
        #list of all index of the tiles occupied by a player's mines
        self.list_tiles_mines = []
        #list containing all the moves made by the player
        self.shot_fired = ['U' for i in range(100)]
        #list of hint for each move made by the player
        self.hint_list = {}
        
        #automatic placement of all ships
        self.place_ships(ship_sizes)
        #automatic placement of all mines
        self.place_mines(nb=mine_nb)
        
    def place_ships(self, sizes=[3,3,3]):
        """Randomly places all the ships
        
        Args:
            sizes (list(int), optional): ship size list. Defaults to [3,3,3].
        """
        for s in sizes:
            
            #creation of the ship
            ship = Ship(size=s)
            
            #while the ship is invalid create another one
            while not ship.check_validity(self.list_tiles_ships):
                ship = Ship(size=s)
            
            #add the newly created ship to the player's ship list
            self.ships.append(ship)
            self.list_tiles_ships.extend(ship.get_occupied_tiles())
            
    def place_mines(self,nb=8):
        """Randomly places all the mines
        
        Args:
            nb (int, optional): number of mines. Defaults 8.
        """
        for x in range(nb):
            mine = Mine()
            while not mine.check_validity(self.mines,self.list_tiles_ships):
                mine = Mine()
                
            self.mines.append(mine)
            self.list_tiles_mines.append(mine.get_index())
    def get_hint_list(self):
        """Return the list of all hint
        hints are in this format, tile index : (hint for ships, hint for mines)
        
        Returns:
            dict(int,tuple(int,int)): dictionnary containing all hint
        """
        return self.hint_list
    
    def add_hint(self,idx,value):
        """Add an hint to the hint list

        Args:
            idx (int): index of the tile
            value (tuple(int,int)): hints about ships and mines 
        """
        self.hint_list[idx]=value        
    
            
    def get_ships(self):
        """Returns the list of all player's ship
        
        Returns:
            list(Ship): player's ship list
        """
        return self.ships
    
    def get_list_tiles_ships(self):
        """Returns the list of indexes of all tiles occupied by a ship
        
        Returns:
            list(int): list of indexes
        """
        return self.list_tiles_ships

    def get_list_tiles_mines(self):
        """Returns the list of indexes of all tiles occupied by a mine
        
        Returns:
            list(int): list of indexes
        """
        return self.list_tiles_mines
    
    def get_shot_fired(self):
        """Returns the list of every moves made by the player
        
        Returns:
            list(char): list of move
        """
        return self.shot_fired
    
    def set_shot_fired(self,idx,value):
        """Update the list of moves made by player 
        
        Args:
            idx (inx): index of the move
            value (char): type of the move
        """
        self.shot_fired[idx]=value
    
    def get_mines(self):
        """
        Returns:
            list(Mine): player's mine list
        """
        return self.mines
    
    def get_name(self):
        """
        Returns:
            String: player's name
        """
        return self.name
    
    def get_hp(self):
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
        return self.hp, color
    
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
    
    
