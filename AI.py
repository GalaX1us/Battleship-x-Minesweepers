from player import Player
from ship import *
from mine import *
from utils import *

class Knowledge():
    """
    A Knowledge consists of a set of board indexs,
    and a count of the number of those indexs which are mines.
    and another count of the number of those indexs which are ships
    """

    def __init__(self, indexs, m_count, s_count):
        self.indexs = set(indexs)
        self.mine_count = m_count
        self.ship_count = s_count

    def __eq__(self, other):
        return self.indexs == other.indexs \
            and self.mine_count == other.mine_count \
            and self.ship_count == other.ship_count

    def __str__(self):
        return f"{self.indexs} : {self.mine_count} mines and {self.ship_count}"

    def known_mines(self):
        """
        Returns the set of all indexs in self.indexs known to be mines.
        """
        pass

    def known_safes(self):
        """
        Returns the set of all indexs in self.indexs known to be safe.
        """
        pass

    def mark_mine(self, index):
        """
        Updates internal knowledge representation given the fact that
        a index is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, index):
        """
        Updates internal knowledge representation given the fact that
        a index is known to be safe.
        """


class PLayerAI(Player):
    """
    Minesweeper game player
    """

    def __init__(self,name,ship_sizes=[3,3,3],mine_nb=8,r_placement=True):

        super.__init__(name,ship_sizes,mine_nb,r_placement)
        
        # Keep track of indexs known to be safe or mines
        self.known_mines = set()
        self.known_safes = set()
        self.known_ships = set()

        # List of sentences about the game known to be true
        self.knowledges = []

    def mark_mine(self, index):
        """
        Marks an tile as a mine, and updates all knowledge
        to mark that index as a mine as well.
        """
        self.known_mines.add(index)
        for sentence in self.knowledges:
            sentence.mark_mine(index)

    def mark_ship(self, index):
        """
        Marks an tile as a ship, and updates all knowledge
        to mark that index as a ship as well.
        """
        self.known_ships.add(index)
        for sentence in self.knowledges:
            sentence.mark_ship(index)
    
    def mark_safe(self, index):
        """
        Marks an index as safe, and updates all knowledge
        to mark that index as safe as well.
        """
        self.known_safes.add(index)
        for sentence in self.knowledges:
            sentence.mark_safe(index)

    def add_knowledge(self, index, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe index, how many neighboring indexs have mines in them.

        This function should:
            1) mark the index as a move that has been made
            2) mark the index as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `index` and `count`
            4) mark any additional indexs as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe index to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among indexs that:
            1) have not already been chosen, and
            2) are not known to be mines
        """