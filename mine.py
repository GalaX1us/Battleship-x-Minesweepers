import random

from utils import *


class Mine():
    def __init__(self,coords=()):
        self.x = random.randrange(0,NB_TILE-1) if not coords else coords[0]
        self.y = random.randrange(0,NB_TILE-1) if not coords else coords[1]
        self.index = self.y*NB_TILE+self.x
    
    def check_validity(self,list_mines,list_ships):
        """Check if this mine placement is valid 

        Args:
            list_mines (list(Mine)): list of mines that have already been placed
            list_ships (list(Ship)): list of ships that have already been placedd

        Returns:
            bool: is the placement valid or not (True/False)
        """
        if self.index in list_mines:
            return False
        elif self.index in list_ships:
            return False
        return True