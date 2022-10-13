import numpy as np
from player import Player
from ship import *
from mine import *
from utils import *

class PlayerAI(Player):
    """
    Self playing AI
    """

    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8):

        super().__init__(name,ship_sizes,mine_nb,True)
        
        self.ready = True

        self.prob_map = np.zeros([10, 10])
        self.shot_map = np.zeros([10, 10])
        
        self.opponent_remaining_sizes=ship_sizes
        
    def add_hint(self, idx, nb_s, nb_m, neib):
        super().add_hint(idx, nb_s, nb_m)
        
        # the tiles as clear because the number of ships in this area is zero
        if nb_s==0:
            for idx in neib:
                x,y = get_coords(idx)
                self.shot_map[y][x]=1
    
    def gen_prob_map(self):
        """
           Generates the grid with, for each cell, its probability to contain a ship
        """
        
        #create a 10 x 10 matrix with only zeros
        prob_map = np.zeros([10, 10])
        
        for ship_s in self.ships_sizes:
            use_size = ship_s - 1
            # check where a ship will fit on the board
            for y in range(NB_TILE):
                for x in range(NB_TILE):
                    
                    # set the probability for misses or explosion to zero
                    if self.moves_made[get_index(x,y)] is Move.MISS or self.moves_made[get_index(x,y)] is Move.EXPLOSION:
                        prob_map[y][x] = 0
                        
                    elif self.moves_made[get_index(x,y)] is Move.UNKNOWN:
                        
                        # get potential ship endpoints
                        endpoints = []
                        
                        if y - use_size >= 0:
                            endpoints.append(((y - use_size, x), (y, x)))
                        if y + use_size <= 9:
                            endpoints.append(((y, x), (y + use_size, x)))
                        if x - use_size >= 0:
                            endpoints.append(((y, x - use_size), (y, x)))
                        if x + use_size <= 9:
                            endpoints.append(((y, x), (y, x + use_size)))

                        for (start_y, start_x), (end_y, end_x) in endpoints:
                            if np.all(self.shot_map[start_y:end_y+1, start_x:end_x+1] == 0):
                                
                                # add 1 to all endpoints to compensate for python indexing
                                # increase probability of attacking tiles where a ship can fits in
                                prob_map[start_y:end_y+1, start_x:end_x+1] += 1
                    
                    # increase probability of attacking tiles near successful hits
                    elif self.moves_made[get_index(x,y)] is Move.HIT:

                        if (y + 1 <= 9) and (self.shot_map[y + 1][x] == 0):
                            if (y - 1 >= 0) and self.moves_made[get_index(x,y-1)] is Move.HIT:
                                prob_map[y + 1][x] += 15
                            else:
                                prob_map[y + 1][x] += 10

                        if (y - 1 >= 0) and (self.shot_map[y - 1][x] == 0):
                            if (y + 1 <= 9) and self.moves_made[get_index(x,y+1)] is Move.HIT:
                                prob_map[y - 1][x] += 15
                            else:
                                prob_map[y - 1][x] += 10

                        if (x + 1 <= 9) and (self.shot_map[y][x + 1] == 0):
                            if (x - 1 >= 0) and self.moves_made[get_index(x-1,y)] is Move.HIT:
                                prob_map[y][x + 1] += 15
                            else:
                                prob_map[y][x + 1] += 10

                        if (x - 1 >= 0) and (self.shot_map[y][x - 1] == 0):
                            if (x + 1 <= 9) and self.moves_made[get_index(x+1,y)] is Move.HIT:
                                prob_map[y][x - 1] += 15
                            else:
                                prob_map[y][x - 1] += 10

        self.prob_map = prob_map
        
    def make_move(self, opponent:Player):
        """
        Automatically makes the AI play

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
        self.shot_map[y][x]=1
        
        return idx

    def find_good_move(self):
        """
        Find the best move that can be done based on the matrix of probability

        Returns:
            tuple(int,int): coords of the best move
        """
        
        self.gen_prob_map()
        
        # gets the index of the largest probability in the matrix
        best_prob = np.where(self.prob_map == np.amax(self.prob_map))
        guess_y, guess_x = best_prob[0][0], best_prob[1][0]
        
        return guess_x, guess_y
        