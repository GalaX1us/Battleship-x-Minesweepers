from board import Board
from mine import *
from ship import *
from utils import *


class Player():
    def __init__(self,name,ships_sizes=[3,3,3],mine_nb=8,r_placement=True):     
        
        self.name = name
        self.max_hp = len(ships_sizes)
        self.hp = self.max_hp
        
        self.ships_sizes = ships_sizes
        self.nb_mines = mine_nb
        
        self.board = Board(self.ships_sizes, self.nb_mines)
        
        #list of hint for each move made by the player
        self.hint_list = {}

        self.has_played = False
                
        if r_placement:
            self.board.place_randomly()
    
    def is_ready(self):
        return self.board.ready
    
    def add_hint(self,idx,nb_s,nb_m):
        self.hint_list[idx]=(nb_s,nb_m)
    
    def add_move(self,idx,value):
        """
        Update the list of moves made by player 
        
        Args:
            idx (inx): index of the move
            value (char): type of the move
        """
        self.board.moves_made[idx]=value
        
    def add_opponent_move(self,idx,value):
        """
        Update the list of moves made by the opponent 
        
        Args:
            idx (inx): index of the move
            value (char): type of the move
        """
        self.board.shots_received[idx]=value
    
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
        
    def getting_shot(self,x,y):
        """
        This method return the result of the opponent shot
        
        Args:
            x (int): horizontal coord
            y (int): vertical coord

        Returns:
            Move, list(int): type of the move and idexes of the ship if it is sunk
        """
        idx = get_index(x,y)
        
        shot = Move.MISS
        sunk_idx = []
        
        if idx in self.board.list_tiles_mines:
            return Move.EXPLOSION, sunk_idx
        
        for ship in self.board.ships:
            if idx in ship.occupied_tiles:
                ship.getting_shot(idx)
                shot = Move.HIT
                
                #check if the ship is sunk
                if ship.sunk:
                    for i in ship.occupied_tiles:
                        sunk_idx.append(i)
                    self.boom()
                    shot = Move.SUNK
                break
        if shot is Move.SUNK:
            for i in sunk_idx:
                self.add_opponent_move(i,Move.SUNK)
        else:
            self.add_opponent_move(idx, shot)
            
        return shot, sunk_idx
        
        
    def make_move(self,x,y,opponent):
        """This function performs the player's move

        Args:
            x (int): horizontal coord of the move
            y (int): vertical coord of the move

        Returns:
            bool:   return False if a move has already been made at this coords and True otherwise
        """
        idx = get_index(x,y)
        
        if self.board.moves_made[idx] is not Move.UNKNOWN:
            return
        
        # check what's the result of the shot
        shot, sunk_idx = opponent.getting_shot(x,y)
        
        # add the shot to the moves made by the player
        if shot is Move.SUNK:
            for i in sunk_idx:
                self.add_move(i,Move.SUNK)
        elif shot is Move.EXPLOSION:
            self.boom()
            self.add_move(idx, shot)
        else:
            self.add_move(idx, shot)
            
        self.has_played=True
    
