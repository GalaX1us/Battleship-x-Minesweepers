import time
from threading import Timer

import pygame
import pygame.freetype

from AI import PlayerAI
from button import Button
from game import Game
from mine import Mine
from player import Player
from ship import Ship
from utils import *

#initialize key components of the game
pygame.init()
pygame.display.set_caption("Battleship X Minesweaper")
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
mainClock = pygame.time.Clock()
logo = pygame.transform.scale(pygame.image.load("assets/images/logo.png"), ((WIDTH/2,WIDTH/2)))
flag = pygame.transform.scale(pygame.image.load("assets/images/flag.png"), ((TILE_SIZE,TILE_SIZE)))

def init_game():
    game = Game()
    main_menu(game)
    
def buttons_draw(button_list):
    """Display all the buttons in button_list

    Args:
        button_list (list(Button)): button list
    """
    #loop through every buttons in button_list and display them
    for b in button_list:
        b.draw()

def draw_text(text, x, y, size = 50, color = (255, 255, 255), font_type = "assets/fonts/FredokaOne-Regular.ttf"):
    """display a text on the screen

    Args:
        text (string): text to display
        x (int): horizontal coords of the text
        y (int): vertical coords of the text
        size (int, optional): size of the font. Defaults to 50.
        color (tuple, optional): color of the text. Defaults to (255, 255, 255).
        font_type (str, optional): font. Defaults to "assets/fonts/FredokaOne-Regular.ttf".
    """
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    SCREEN.blit(text, (x, y))
        
def draw_grid(x_offset=0,y_offset=INFO_MARGIN_HEIGHT):
    """display a grid on the screen

    Args:
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
    """
    #loop NB_TILE**2 fois
    for i in range(NB_TILE**2):
        
        #compute tile's pixel coords
        x = i%NB_TILE*TILE_SIZE+x_offset
        y = i//NB_TILE*TILE_SIZE+y_offset
        
        #create and display the square
        square = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width=3)
        
def draw_moves_made(player:Player,game:Game, x_offset=0,y_offset=INFO_MARGIN_HEIGHT,search=True):
    """
    display all the moves that a specific player have done since the begining

    Args:
        player (Player): player whose moves are to be displayed
        game (Game): game instance
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
        search (bool, optional): option that define the radius of the displayed shot
                                    if false, opponents shots are shown. Defaults to True.
    """
    #option that define the radius of the displayed shot
    rad = TILE_SIZE//2-INDENT if search else TILE_SIZE//5
    
    moves = player.board.moves_made if search else player.board.shots_received
        
    #loop through all moves made
    for i in range(NB_TILE**2):
               
        #get the move which was made on index i
        mv = moves[i]
        
        #if a move was made
        if mv is not Move.UNKNOWN:
            
            #compute pixel coords
            x=i%NB_TILE*TILE_SIZE+x_offset
            y=i//NB_TILE*TILE_SIZE+y_offset
            
            #if the move was a mine explosion
            if mv is Move.EXPLOSION:
                #display an inactive mine
                pygame.draw.circle(SCREEN, MOVE_COLOR[mv][0], (x+TILE_SIZE//2,y+TILE_SIZE//2), rad)
                draw_text('X', x+18, y+8,size=45,color=MOVE_COLOR[mv][1])
            elif mv is Move.FLAG:
                SCREEN.blit(flag, (x,y))
            else:
                
                #display a circle with a color corresponding to a certain type of move 
                pygame.draw.circle(SCREEN, MOVE_COLOR[mv], (x+TILE_SIZE//2,y+TILE_SIZE//2), rad)
            
                #if the move was a miss, display the infos of the surrounding tiles (radius 2)
                if mv is Move.MISS and game.show_search_grid and game.hint_option<=2 and game.hint_radius:
                    
                    #display only ships hints
                    if game.hint_option == 0:
                        draw_text(str(player.hint_list[i][0]), x+7, y,size=30,color=ELEMENT_COLOR["Ship"])
                    
                    #display only mines hints
                    elif game.hint_option == 1:
                        draw_text("{0:>2}".format(str(player.hint_list[i][1])), x+35, y+32,size=30,color=ELEMENT_COLOR["Mine"])
                    
                    #display both
                    else:
                        draw_text(str(player.hint_list[i][0]), x+7, y,size=30,color=ELEMENT_COLOR["Ship"])
                        draw_text("{0:>2}".format(str(player.hint_list[i][1])), x+35, y+32,size=30,color=ELEMENT_COLOR["Mine"])
                    
            
        
def draw_ships(player:Player, x_offset=0, y_offset=INFO_MARGIN_HEIGHT, sunk_ship=False):
    """draw ships on the screen

    Args:
        player (Player): player whose ships are to be displayed
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
        sunk_ship (bool, optional): only show sunk ships. Defaults to False.
    """
    
    #loop through player's ships
    for ship in player.board.ships:
        
        #skip ships that are not sunk if option is True
        if sunk_ship and not ship.sunk:
            continue
        
        #copmute pixel coords
        x = ship.x*TILE_SIZE+INDENT
        y = ship.y*TILE_SIZE+INDENT
        
        #compute width and height of the ship
        if ship.orientation == 'H':
            width = ship.size*TILE_SIZE -2*INDENT
            height = TILE_SIZE -2*INDENT
        else:
            width = TILE_SIZE -2*INDENT
            height = TILE_SIZE*ship.size -2*INDENT
        
        #draw the ship
        rec = pygame.Rect(x+x_offset, y+y_offset, width, height)
        
        #set different colors for normal and sunk ship 
        color = RED if sunk_ship else L_GREY
        
        #display the sip on the screen
        pygame.draw.rect(SCREEN, color , rec, border_radius=50)

def draw_mines(player: Player, x_offset=0, y_offset=INFO_MARGIN_HEIGHT):
    """draw mines on the screen

    Args:
        player (Player): player whose mines are to be displayed
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
    """
    
    #loop through all player's mines
    for mine in player.board.mines:
        
        #compute next mine pixel coords
        x = mine.x*TILE_SIZE+TILE_SIZE/2
        y = mine.y*TILE_SIZE+TILE_SIZE/2
        
        #draw a circle corresponding to a mine
        pygame.draw.circle(SCREEN, YELLOW, (x+x_offset,y+y_offset), TILE_SIZE//2-INDENT)
        
def show_single_ship(size,coords,orient):
    x = coords[0]*TILE_SIZE+INDENT
    y = coords[1]*TILE_SIZE+INDENT+INFO_MARGIN_HEIGHT
    
    #compute width and height of the ship
    if orient == 'H':
        width = size*TILE_SIZE -2*INDENT
        height = TILE_SIZE -2*INDENT
    else:
        width = TILE_SIZE -2*INDENT
        height = TILE_SIZE*size -2*INDENT
    
    #draw the ship
    rec = pygame.Rect(x, y, width, height)
        
    #display the sip on the screen
    pygame.draw.rect(SCREEN, L_GREY , rec, border_radius=50)
    
def show_single_mine(coords):
    x = coords[0]*TILE_SIZE+TILE_SIZE/2
    y = coords[1]*TILE_SIZE+TILE_SIZE/2+INFO_MARGIN_HEIGHT
    
    #draw a circle corresponding to a mine
    pygame.draw.circle(SCREEN, YELLOW, (x,y), TILE_SIZE//2-INDENT)

def draw_search_grid(game:Game):
    """display current player searching grid

    Args:
        game (Game): game instance
    """
    #display grid
    draw_grid()
    #display opponent sunk ships
        
    #display the moves made by the current player
    draw_moves_made(game.current_player,game)


def draw_player_grid(game:Game):
    """display current player own grid      

    Args:
        game (Game): game instance
    """
    #display grid
    draw_grid()
    #display player own ships
    draw_ships(game.current_player)
    #display player own mines
    draw_mines(game.current_player)
    #display the moves made by the opponent
    draw_moves_made(game.current_player,game,search=False)
    
    
def main_loop(game:Game, AI=0):
    """
        Main loop of the game, display the game grid
    """    
    #game initialisation
    game.init_players(AI)
    if not game.random_placement and AI!=2:
        placement_menu(game)
    running = True
    
    #buttons creation
    buttons = []
    
    Next = Button("Next", 50,game.next_round,WIDTH/3,75,(WIDTH/3,15),SCREEN,colorB=GREEN)
    
    buttons.append(Button("Search grid", 50,game.switch_grid,WIDTH/2,75,(WIDTH/4,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN, 
                          text_switch=["Your grid"],colorB=GREEN))
    if not game.hint_radius:
        buttons.append(Button("None", 50,useless,WIDTH/4,75,(0,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN,colorB=BLUE))
    else:
        buttons.append(Button("Ship", 50,game.switch_hint,WIDTH/4,75,(0,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN, 
                          text_switch=["Mine","Both","None"],colorB=BLUE))
    buttons.append(Button("Quit", 50,quit,WIDTH/4,75,(3*WIDTH/4,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN,colorB=RED))
    
    #main loop
    while running:
        
        #handle user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                quit()
            
            #allows you to leave the game by pressing space when the game is over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.over:
                    running=False
                    init_game()
            
            #get mouse clik
            if event.type == pygame.MOUSEBUTTONDOWN and not game.over and type(game.current_player)!=PlayerAI:
                
                #get mouse coords
                location = pygame.mouse.get_pos()
                x,y,validity=get_position(location[0], location[1])
                
                #check if coords are valid and correspond to a specific tile
                if validity and game.show_search_grid :
                    if pygame.mouse.get_pressed()[0] and not game.pause:
                    
                        #play or not the player's move depending on whether the same move has already been played
                        game.play(x,y)
                
                    if pygame.mouse.get_pressed()[2]:
                        game.current_player.board.place_flag(x,y)
           
        if type(game.current_player)==PlayerAI and not game.over and not game.pause:
            game.play()   
            
        #fill screen background                  
        SCREEN.fill(GREY)
        
        #allows you to choose between the two display modes
        if game.show_search_grid:
            draw_search_grid(game)
            
        else:
            draw_player_grid(game)
            
        if game.over:
            #display a game over message
            if game.current_player.hp==0:
                game.change_player()
            draw_text(f"{game.current_player.name} Won !", (1/4)*WIDTH-35, 0,size=80, color=GREEN)
        else:       
            #display current playe name and health points
            draw_text(game.current_player.name, 20, 5,size=70)
            draw_text("{:>2d}HP".format(game.current_player.hp), WIDTH-165, 5,size=70,color=game.current_player.get_hp_color())
        
        #display buttons
        buttons_draw(buttons)
        
        #moves on to the next round
        if game.current_player.has_played and not game.over and not game.pause:
            game.pause=True
            if type(game.current_player)==PlayerAI:
                t = Timer(1.0, game.next_round)
                t.start()
            
        if type(game.current_player)==Player and game.pause and not game.over and game.current_player.has_played:
            Next.draw()
        
        #update screen
        pygame.display.update()
        mainClock.tick(FPS)

def placement_menu(game:Game):
    #buttons creation
    buttons = []
    buttons.append(Button("Ship", 50,game.switch_placement_type,WIDTH/4,75,(0,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN, 
                          text_switch=["Mine"],colorB=BLUE))
    buttons.append(Button("Quit", 50,quit,WIDTH/4,75,(3*WIDTH/4,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN,colorB=RED))
    
    orient = 'V'
    
    #main loop of the function
    running = True
    while running:
        
        curr=game.current_player
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    orient = 'H' if orient=='V' else 'V'
            #get mouse clik
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if pygame.mouse.get_pressed()[2]:
                    orient = 'H' if orient=='V' else 'V'
                    
                elif pygame.mouse.get_pressed()[0]:
                    
                    #get mouse coords
                    location = pygame.mouse.get_pos()
                    x,y,validity=get_position(location[0], location[1])
                    
                    #check if coords are valid and correspond to a specific tile
                    if validity and not curr.is_ready():
                        
                        if game.placement_type == "Ship" and not curr.board.ships_ready():
                        
                            s=curr.ships_sizes[len(curr.board.ships)]
                            curr.board.place_ship(s,(x,y),orient)
                            
                        elif game.placement_type == "Mine" and not curr.board.mines_ready():
                            curr.board.place_mine((x,y))
                                    
        
        #fill screen background
        SCREEN.fill(GREY)
        
        #draw grid
        draw_player_grid(game)
        
        #get mouse coords
        location = pygame.mouse.get_pos()
        x,y,validity=get_position(location[0], location[1])
        
        if validity and not curr.is_ready():
            
            if game.placement_type == "Ship" and not curr.board.ships_ready():
                s=curr.ships_sizes[len(curr.board.ships)]
                if Ship(s,(x,y),orient).check_validity(curr.board.list_tiles_ships,curr.board.list_tiles_mines):
                    
                    show_single_ship(s,(x,y),orient)
                    
            elif game.placement_type == "Mine" \
                and not curr.board.mines_ready() \
                and Mine((x,y)).check_validity(curr.board.list_tiles_mines,curr.board.list_tiles_ships):
                    
                show_single_mine((x,y))
        
        draw_text("Placement phase", 110, 5,size=70,color=BLUE)
        
        #display current player name
        draw_text(curr.name, 20, 5,size=70,color=GREEN)
        if game.placement_type=="Ship":
            draw_text("{:<2} Left".format(game.nb_ships-len(curr.board.ships)), 235, 800,size=70,color=BLUE)
        else:
            draw_text("{:<2} Left".format(game.nb_mines-len(curr.board.mines)), 235, 800,size=70,color=BLUE)
        
        #show buttons
        buttons_draw(buttons)
        
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)
        
        if curr.is_ready() and game.current_opponent.is_ready():
            game.change_player()
            time.sleep(2)
            running=False
            
        elif curr.is_ready():
            game.change_player()
        

def help_menu(game:Game):
    """
        loop and window displaying a visual aid to understand the color code of the game
    """
    
    #buttons creation
    buttons = []
    buttons.append(Button('Main menu', 50,main_menu,500,80,(100,750),SCREEN,event_args=(game,)))
    
    #main loop of the function
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
        
        #fill screen background
        SCREEN.fill(GREY)
        
        #ship background
        rec = pygame.Rect(55, 30 , 3*TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, ELEMENT_COLOR["Ship"] , rec, border_radius=50)
        draw_text("Ships", 320, 35, color=ELEMENT_COLOR["Ship"])
        
        #mine help   
        pygame.draw.circle(SCREEN, ELEMENT_COLOR["Mine"], (225,160), 40)
        draw_text("Mines", 320, 135, color=ELEMENT_COLOR["Mine"])
        
        #exploded mine help
        pygame.draw.circle(SCREEN, MOVE_COLOR[Move.EXPLOSION][0], (225,265), 40)
        draw_text('X', 191,210,size=90,color=MOVE_COLOR[Move.EXPLOSION][1])
        draw_text("Exploded", 320, 235, color=MOVE_COLOR[Move.EXPLOSION][1])
        
        #hit help
        pygame.draw.circle(SCREEN, MOVE_COLOR[Move.HIT], (225,365), 40)
        draw_text("Hit", 320, 335, color=MOVE_COLOR[Move.HIT])
        
        #sunk help
        rec2 = pygame.Rect(55, 430 , 3*TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, MOVE_COLOR[Move.SUNK] , rec2, border_radius=50)
        draw_text("Sunk", 320, 435, color=MOVE_COLOR[Move.SUNK])
        
        #missed help
        pygame.draw.circle(SCREEN, MOVE_COLOR[Move.MISS], (225,565), 40)
        draw_text("Missed", 320, 535, color=MOVE_COLOR[Move.MISS])
        
        SCREEN.blit(pygame.transform.scale(flag,(100,100)), (180,625))
        draw_text("Flag", 320, 635, color=RED)
        
        #show buttons
        buttons_draw(buttons)
        
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)

    
def settings_menu(game:Game):
    """
        loop and window that allow the user to tweaks the settings of the game
    """
    #creation of the buttons
    buttons = []
    buttons.append(Button('Main menu', 50,main_menu,500,80,(100,750),SCREEN,event_args=(game,)))
    buttons.append(Button('-', 100,game.change_hint_radius,100,100,(100,70),SCREEN,event_args=(-1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    buttons.append(Button('+', 100,game.change_hint_radius,100,100,(500,70),SCREEN,event_args=(1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    buttons.append(Button('<', 100,game.switch_random_placement,100,100,(100,250),SCREEN))
    buttons.append(Button('>', 100,game.switch_random_placement,100,100,(500,250),SCREEN))
    buttons.append(Button('-', 100,game.change_ship_nb,100,100,(100,430),SCREEN,event_args=(-1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    buttons.append(Button('+', 100,game.change_ship_nb,100,100,(500,430),SCREEN,event_args=(1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    buttons.append(Button('-', 100,game.change_mine_nb,100,100,(100,610),SCREEN,event_args=(-1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    buttons.append(Button('+', 100,game.change_mine_nb,100,100,(500,610),SCREEN,event_args=(1,),
                          font="assets/fonts/EricaOne-Regular.ttf"))
    
    #main loop of the gfunction
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
        
            
        SCREEN.fill(GREY)
        
        #show title
        
        draw_text( "Hint radius", 215, 0, size=50, color=BLUE)
        draw_text( str(game.hint_radius), 325, 65, size=80, color=BLUE)
        
        draw_text( "Random placement", 120, 180, size=50, color=BLUE)   
            
        if game.random_placement:
            draw_text("On", 300,250, size=70, color=GREEN)
        else:
            draw_text("Off", 290,250, size=70, color=RED)
            
        draw_text( "Number of ships", 155, 360, size=50, color=BLUE)
        draw_text( str(game.nb_ships), 325, 430, size=80, color=BLUE)
        
        draw_text( "Number of mines", 145, 540, size=50, color=BLUE)
        draw_text( str(game.nb_mines), 325, 610, size=80, color=BLUE)
        
        #show buttons
        buttons_draw(buttons)
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)

def main_menu(game:Game):
    """
       loop and window that manage the start menu 
    """
    #creation of the buttons
    buttons = []
    buttons.append(Button('Player Vs Player', 50,main_loop,500,80,(100,450),SCREEN,event_args=(game,))) 
    buttons.append(Button('Player Vs AI', 50,main_loop,500,80,(100,550),SCREEN,event_args=(game,1)))
    buttons.append(Button('AI Vs AI', 50,main_loop,500,80,(100,650),SCREEN,event_args=(game,2))) 
    buttons.append(Button('Settings', 50,settings_menu,245,80,(228,750),SCREEN,event_args=(game,))) 
    buttons.append(Button('Help', 50,help_menu,120,80,(100,750),SCREEN,event_args=(game,))) 
    buttons.append(Button('Exit', 50,exit,120,80,(480,750),SCREEN)) 
    
    #main loop of the gfunction
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
                
            
        SCREEN.fill(GREY)
        
        #show title
        draw_text( "Battle Ship", 60, HEIGHT/3, size=110, color=BLUE)
        #show logo
        SCREEN.blit(logo, (WIDTH/4,-30))
        #show buttons
        buttons_draw(buttons)
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)

if __name__ == "__main__":
    init_game()