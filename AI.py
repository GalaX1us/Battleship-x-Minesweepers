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

    def __init__(self, cells, m_count, s_count):
        self.cells = set(cells)
        self.mine_count = m_count
        self.ship_count = s_count

    def __eq__(self, other):
        return self.cells == other.cells \
            and self.mine_count == other.mine_count \
            and self.ship_count == other.ship_count

    def __str__(self):
        return f"{self.cells} : {self.mine_count} mines and {self.ship_count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        pass

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        pass

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """


class PLayerAI(Player):
    """
    Minesweeper game player
    """

    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8,r_placement=True):

        super.__init__(name,ship_sizes,mine_nb,r_placement)
        
        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """