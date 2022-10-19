import time

import click

from AI import PlayerAI
from game import Game

# This program aims to test the performance of different types of AI
# on different types of game (diff settings)
  


# ==== Settings ====
NB_GAME = 1000
NB_MINE=0
SHIP_SIZES=[5,4,3,2]
RESULT_FILE = "results_test_perf.txt"
AI_VERSION = "Prob Map V3"
# ==================

game_rounds_list = []
game_winners_list = []

global_start = time.perf_counter()

print("Performance test in progress ...")

# this is a live progress bar with a "time left" counter
with click.progressbar(range(NB_GAME),fill_char='█',bar_template="[%(bar)s]  %(info)s") as bar:
    for i in bar:
        
        # init the i-th game 
        game = Game()
        
        # init the i-th players
        game.player1 = PlayerAI("AI(1)",SHIP_SIZES,NB_MINE)
        game.player2 = PlayerAI("AI(2)",SHIP_SIZES,NB_MINE)       
        game.current_player = game.player1
        game.current_opponent = game.player2
        
        # play until the end
        while not game.over:
            game.play()
            game.next_round()
        
        # save stats of the i-th game
        game_rounds_list.append(game.rounds)
        game_winners_list.append(game.winner.name)
    
global_end = time.perf_counter()

# write stats in the result file
with open(RESULT_FILE, "a") as fichier:
    fichier.write("====================================\n")
    fichier.write("AI version : {}\n".format(AI_VERSION))
    fichier.write("Settings : number of games = {}, ships = {}, mines = {}\n".format(NB_GAME,SHIP_SIZES,NB_MINE))
    fichier.write("Took {:.5f} secs (mean = {:.5f})\n".format(global_end-global_start,(global_end-global_start)/NB_GAME))
    fichier.write("AI(1) Win rate : {:.2f}%\n".format(game_winners_list.count("AI(1)")/NB_GAME*100))
    fichier.write("Rounds stats : mean = {:>3}, max = {}, min = {}\n".format(sum(game_rounds_list)/len(game_rounds_list),max(game_rounds_list),min(game_rounds_list)))
    fichier.write("====================================\n\n")
    

print("Performance test completed !")
print("The results have been saved in {}".format(RESULT_FILE))
