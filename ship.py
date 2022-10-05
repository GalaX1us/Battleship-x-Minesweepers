import random
from utils import *

class Ship():
    
    def __init__(self,size=3,coords=(),orient=''):
        
        #horizontal coord of the ship
        self.x = random.randrange(0,9) if not coords else coords[0]
        #vertical coord of the ship
        self.y = random.randrange(0,9) if not coords else coords[1]
        #orientation of the ship (Horizontal, vertical)
        self.orientation = random.choice(['H','V']) if not orient else orient
        
        #size of the ship
        self.size = size
        
        #indexes of the tiles occupied by the ship
        self.occupied_tiles = self.compute_occupied_tiles()
        
        #list of tiles that have been hit
        self.hit_tiles = []
        
        #is the ship sunk 
        self.sunk=False
    
    def compute_occupied_tiles(self):
        """Compute all indexes occupied by the ship from it's coords and orientation
        
        Returns:
            list(int): list of all indexes occupied by the ship
        """
        idx = get_index(self.x, self.y)
        if self.orientation == 'H':
            return [idx + i for i in range(self.size)]
        elif self.orientation == 'V':
            return [idx + i*10 for i in range(self.size)]
        
    def check_validity(self,ship_list,mine_list):
        """Check if this ship has a valid placement
        
        Args:
            ship_list (list(int)): list of indexes of all ships that has already been placed
            mine_list (list(int)): list of indexes of all mines that has already been placed

        Returns:
            bool: is the placement valid (True/False)
        """
        #looping through all indexes occupied by the ship
        for tile in self.occupied_tiles:
            if tile>=100:
                return False
            
            #check if the ship starts at the end of the line and continues to the beginning of the line below
            if (tile//10)!=self.y and (tile%10)!=self.x:
                return False
            
            #check if the ship overlaps a ship already placed before
            if tile in ship_list:
                return False
            
            if tile in mine_list:
                return False
                
        return True
    
    def getting_shot(self,idx):
        """Register a shot on a particular index
        
        Args:
            idx (int): index of the shot
        """
        self.hit_tiles.append(idx)
        if len(self.hit_tiles)==self.size:
            self.sunk=True