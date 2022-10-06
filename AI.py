import numpy as np
from player import Player
from ship import *
from mine import *
from utils import *

class PlayerAI(Player):
    """
    Minesweeper game player
    """

    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8):

        super().__init__(name,ship_sizes,mine_nb,True)
        
        self.ready = True

        self.prob_map = np.zeros([10, 10])
        self.shot_map = np.zeros([10, 10])
    
    def gen_prob_map(self):
        """
           Generates the grid with for each cell its probability to contain a ship
        """
        
        #create a 10 x 10 matrix with only zeros
        prob_map = np.zeros([10, 10])
        
        for ship_s in self.ships_to_be_placed:
            use_size = ship_s - 1
            # check where a ship will fit on the board
            for y in range(NB_TILE):
                for x in range(NB_TILE):
                    if self.moves_made[get_index(x,y)] == 'U':
                        # get potential ship endpoints
                        endpoints = []
                        
                        # add 1 to all endpoints to compensate for python indexing
                        if y - use_size >= 0:
                            endpoints.append(((y - use_size, x), (y + 1, x + 1)))
                        if y + use_size <= 9:
                            endpoints.append(((y, x), (y + use_size + 1, x + 1)))
                        if x - use_size >= 0:
                            endpoints.append(((y, x - use_size), (y + 1, x + 1)))
                        if x + use_size <= 9:
                            endpoints.append(((y, x), (y + 1, x + use_size + 1)))

                        for (start_y, start_x), (end_y, end_x) in endpoints:
                            if np.all(self.shot_map[start_y:end_y, start_x:end_x] == 0):
                                prob_map[start_y:end_y, start_x:end_x] += 1

                    # increase probability of attacking tiles near successful hits
                    if self.moves_made[get_index(x,y)]=='H':

                        if (y + 1 <= 9) and (self.shot_map[y + 1][x] == 0):
                            if (y - 1 >= 0) and self.moves_made[get_index(x,y-1)]=='H':
                                prob_map[y + 1][x] += 15
                            else:
                                prob_map[y + 1][x] += 10

                        if (y - 1 >= 0) and (self.shot_map[y - 1][x] == 0):
                            if (y + 1 <= 9) and self.moves_made[get_index(x,y+1)]=='H':
                                prob_map[y - 1][x] += 15
                            else:
                                prob_map[y - 1][x] += 10

                        if (x + 1 <= 9) and (self.shot_map[y][x + 1] == 0):
                            if (x - 1 >= 0) and self.moves_made[get_index(x-1,y)]=='H':
                                prob_map[y][x + 1] += 15
                            else:
                                prob_map[y][x + 1] += 10

                        if (x - 1 >= 0) and (self.shot_map[y][x - 1] == 0):
                            if (x + 1 <= 9) and self.moves_made[get_index(x+1,y)]=='H':
                                prob_map[y][x - 1] += 15
                            else:
                                prob_map[y][x - 1] += 10

                    # decrease probability for misses to zero
                    elif self.moves_made[get_index(x,y)]=='M' or self.moves_made[get_index(x,y)]=='E':
                        prob_map[y][x] = 0

        self.prob_map = prob_map
        
    def make_move(self, opponent:Player):
        """automatically makes the AI play

        Args:
            opponent (Player): current opponent

        Returns:
            int: index of the move
        """
        
        missed=True
        x,y = self.find_good_move()
        idx = get_index(x,y)
        
        
        if idx in opponent.list_tiles_mines:
            self.boom()
            self.add_move(idx, 'E')
            missed=False
        
        for ship in opponent.ships:
            if idx in ship.occupied_tiles:
                ship.getting_shot(idx)
                self.add_move(idx, 'H')
                
                #check if the ship is sunk
                if ship.sunk:
                    for i in ship.occupied_tiles:
                        self.add_move(i, 'S')
                    opponent.boom()
                missed=False
                break
        
        if missed:
            self.add_move(idx, 'M')
        
        self.has_played=True
        self.shot_map[y][x]=1
        
        return idx

    def find_good_move(self):
        
        self.gen_prob_map()
        
        best_prob = np.where(self.prob_map == np.amax(self.prob_map))
        guess_y, guess_x = best_prob[0][0], best_prob[1][0]
        
        return guess_x, guess_y
        