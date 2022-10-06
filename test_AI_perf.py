from game import Game
from AI import PlayerAI
import time

NB_GAME = 100
NB_MINE=8
SHIP_SIZES=[3,3,3]

game_rounds_list = []

global_start = time.perf_counter()

for i in range(NB_GAME):
    local_start = time.perf_counter()
    game = Game()
    
    game.player1 = PlayerAI("AI(1)",SHIP_SIZES,NB_MINE)
    game.player2 = PlayerAI("AI(2)",SHIP_SIZES,NB_MINE)       
    game.current_player = game.player1
    game.current_opponent = game.player2
    
    while not game.over:
        game.play()
        game.next_round()
        
    local_end = time.perf_counter()
    game_rounds_list.append(game.rounds)
    print("Game {:>3} =======> {:.5f} secs and {} rounds".format(i+1,local_end-local_start,game.rounds))
    
global_end = time.perf_counter()
print("Took {} secs to play {} games".format(global_end-global_start,NB_GAME))
print("Mean : "+str(sum(game_rounds_list)/len(game_rounds_list))+" rounds")