from mine import *
from ship import *
from utils import *


class Board():
    """
    Board of a player
    """
    def __init__(self,ships_sizes,mine_nb):
        self.ships_sizes = ships_sizes
        self.nb_mines = mine_nb
        
        self.ships = set()
        self.list_tiles_ships = set()
        
        self.mines = set()
        self.list_tiles_mines = set()
        
        #list containing all the moves made by the player
        self.moves_made = [Move.UNKNOWN for i in range(NB_TILE**2)]
        
        #list containing all the moves made by the opponent
        self.shots_received = [Move.UNKNOWN for i in range(NB_TILE**2)]
        
        self.ready = False
    
    def ships_ready(self):
        return len(self.ships)==len(self.ships_sizes)
    
    
    def mines_ready(self):
        return len(self.mines)==self.nb_mines
    
    def check_ready(self):
        """
        return true if all ships and mines are placed
        """
        if len(self.ships)==len(self.ships_sizes) and len(self.mines) == self.nb_mines:
            self.ready = True
        
    def place_randomly(self):
        """
        Randomly places ships and mines on the board
        """
        self.auto_place_mines()
        self.auto_place_ships()
        self.ready = True
        
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
            self.list_tiles_mines.add(mine.index)
            self.check_ready()
            
    def auto_place_ships(self):
        """Randomly places all the ships
        
        Args:
            sizes (list(int), optional): ship size list. Defaults to [3,3,3].
        """
        for s in self.ships_sizes:
            
            #creation of the ship
            ship = Ship(size=s)
            
            #while the ship is invalid create another one
            while not ship.check_validity(self.list_tiles_ships,self.list_tiles_mines):
                ship = Ship(size=s)
            
            #add the newly created ship to the player's ship list
            self.ships.add(ship)
            self.list_tiles_ships.update(ship.occupied_tiles)
            
    def auto_place_mines(self):
        """Randomly places all the mines
        
        Args:
            nb (int, optional): number of mines. Defaults 8.
        """
        for x in range(self.nb_mines):
            mine = Mine()
            while not mine.check_validity(self.list_tiles_mines,self.list_tiles_ships):
                mine = Mine()
                
            self.mines.add(mine)
            self.list_tiles_mines.add(mine.index)
            
    def place_flag(self,x,y):
        """
        Place a flag on a specific tile.

        Args:
            x (int): horizontal coord
            y (int): vertical coord
        """
        idx = get_index(x,y)
        if self.moves_made[idx] is Move.UNKNOWN:
            self.moves_made[idx]=Move.FLAG
        elif self.moves_made[idx] is Move.FLAG:
            self.moves_made[idx]=Move.UNKNOWN