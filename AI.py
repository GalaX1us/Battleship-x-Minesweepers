from socket import if_nametoindex
from player import Player
from ship import *
from mine import *
from utils import *

class Knowledge():
    """
    A Knowledge consists of a set of board cells,
    and a count of the number of those cells which are mines.
    and another count of the number of those cells which are ships
    """

    def __init__(self, cells, s_count, m_count):
        self.cells = set(cells)
        self.mine_count = m_count
        self.ship_count = s_count

    def __eq__(self, other):
        return self.cells == other.cells \
            and self.mine_count == other.mine_count \
            and self.ship_count == other.ship_count

    def __str__(self):
        return f"{self.cel} : {self.mine_count} mines and {self.ship_count}"       

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.mine_count:
            return self.cells
        return None
    
    def known_ships(self):
        """
        Returns the set of all cells in self.cells known to be ships.
        """
        if len(self.cells) == self.ship_count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.mine_count == 0 and self.ship_count==0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.mine_count -= 1
    
    def mark_ship(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a ship.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.ship_count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)



class PlayerAI(Player):
    """
    Minesweeper game player
    """

    def __init__(self,ship_sizes=[3,3,3],mine_nb=8):

        super.__init__("AI",ship_sizes,mine_nb,True)
        
        # Keep track of cells known to be safe or mines
        self.known_mines = set()
        self.known_ships = set()
        self.known_safes = set()

        # List of knowledges about the game known to be true
        self.knowledge_list = []
        
    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.known_mines.add(cell)
        for knowledge in self.knowledge_list:
            knowledge.mark_mine(cell)
    
    def mark_ship(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.known_ships.add(cell)
        for knowledge in self.knowledge_list:
            knowledge.mark_ship(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.known_safes.add(cell)
        for knowledge in self.knowledge_list:
            knowledge.mark_safe(cell)

    def add_knowledge(self,neighbors,ship_count,mine_count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        
        new_knowledge_cells = []
        s_count = ship_count
        m_count = mine_count

        for n in neighbors:
            if n in self.known_mines:
                m_count-=1
                continue
            elif n in self.known_ships:
                s_count-=1
                continue
            
            if n not in self.moves_made_indexes and n not in self.known_safes:
                new_knowledge_cells.append(n)

        new_knowledge = Knowledge(new_knowledge_cells, s_count,m_count)
        self.knowledge_list.append(new_knowledge)

        new_inferences = []
        for s in self.knowledge_list:
            if s == new_knowledge:
                continue
            elif s.cells.issuperset(new_knowledge.cells):
                setDiff = s.cells-new_knowledge.cells
                # Known safes
                if s.mine_count == new_knowledge.mine_count:
                    for safe in setDiff:
                        self.mark_safe(safe)
                # Known mines
                elif len(setDiff) == s.mine_count - new_knowledge.mine_count:
                    for mine in setDiff:
                        self.mark_mine(mine)
                
                elif len(setDiff) == s.ship_count - new_knowledge.ship_count:
                    for ship in setDiff:
                        self.mark_ship(ship)
                # Known inference
                else:
                    new_inferences.append(Knowledge(setDiff, s.ship_count - new_knowledge.ship_count,s.mine_count - new_knowledge.mine_count))
                    
            elif new_knowledge.cells.issuperset(s.cells):
                setDiff = new_knowledge.cells-s.cells
                # Known safes
                if s.mine_count == new_knowledge.mine_count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Known mines
                elif len(setDiff) == new_knowledge.mine_count - s.mine_count:
                    for mine in setDiff:
                        self.mark_mine(mine)
                
                elif len(setDiff) == new_knowledge.ship_count - s.ship_count:
                    for ship in setDiff:
                        self.mark_ship(ship)
                # Known inference
                else:
                    new_inferences.append(Knowledge(setDiff, new_knowledge.ship_count - s.ship_count,new_knowledge.mine_count - s.mine_count))

        self.knowledge_list.extend(new_inferences)
        self.optimize_knowledge()
    
    def add_move(self, idx, value):
        super().add_move(idx, value)
        if value == 'E':
            self.mark_mine(idx)
        elif value == 'S':
            self.mark_ship(idx)
        else:
            self.mark_safe(idx)
    
    def add_hint(self, idx,neib,nb_s,nb_m):
        super().add_hint(idx, nb_s, nb_m)
        self.add_knowledge(neib,nb_s,nb_m)

    def make_move(self, opponent:Player):
        
        missed=True
        idx = self.find_good_move()
        
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
            
        return idx

    def find_good_move(self):
        
        best_moves = self.known_ships-self.moves_made_indexes
        second_best = self.known_safes-self.moves_made_indexes
        random_move = {x for x in range(100)}-self.moves_made_indexes-self.known_mines
        if len(best_moves) > 0:
            return random.choice(best_moves)
        elif len(second_best>0):
            return random.choice(second_best)
        else:
            return random.choice(random_move)

    def optimize_knowledge(self):
        
        knowledge_optimized = []

        for knowledge in self.knowledge_list:
            k_safes = knowledge.known_safes()
            k_mines = knowledge.known_mines()
            k_ships = knowledge.known_ships()
            
            if k_safes:
                self.knowledge_list.remove(knowledge)
                for safe in k_safes:
                    self.mark_safe(safe)

            elif k_ships:
                self.knowledge_list.remove(knowledge)
                for ship in k_ships.union(self.known_ships):
                    self.mark_ship(ship)
            
            elif k_mines:
                self.knowledge_list.remove(knowledge)
                for mine in k_mines.union(self.known_mines):
                    self.mark_mine(mine)
            
            elif knowledge not in knowledge_optimized:
                knowledge_optimized.append(knowledge)
        
        self.knowledge_list = knowledge_optimized