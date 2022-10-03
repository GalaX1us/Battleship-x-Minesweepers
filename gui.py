import pygame
import pygame.freetype
import sys
from player import Player
from ship import Ship
import random
from game import Game
import time
from button import Button
from utils import *


#initialize key components of the game
pygame.init()
pygame.display.set_caption("Bataille Navale X Démineur")
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
mainClock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)
logo = pygame.transform.scale(pygame.image.load("assets/images/logo.png"), ((WIDTH/2,WIDTH/2)))

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
        
def draw_shot_fired(player,game, x_offset=0,y_offset=INFO_MARGIN_HEIGHT,search=True):
    """display all the moves that a specific player have done since the begining

    Args:
        player (Player): player whose moves are to be displayed
        game (Game): game instance
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
        search (bool, optional): option that define the radius of the displayed shot. Defaults to True.
    """
    #option that define the radius of the displayed shot
    rad = TILE_SIZE//2-INDENT if search else TILE_SIZE//5
        
    #loop through all indexes
    for i in range(NB_TILE**2):
        
        #compute pixel coords
        x=i%NB_TILE*TILE_SIZE+x_offset
        y=i//NB_TILE*TILE_SIZE+y_offset
        
        #get the move which was made on index i
        symbol = player.get_shot_fired()[i]
        
        #if a move was made
        if symbol != 'U':
            
            #if the move was a mine explosion
            if symbol == 'E':
                #display an inactive mine
                pygame.draw.circle(SCREEN, MOVE_COLOR[symbol][0], (x+TILE_SIZE//2,y+TILE_SIZE//2), rad)
                draw_text('X', x+18, y+8,size=45,color=MOVE_COLOR[symbol][1])
            else:
                
                #display a circle with a color corresponding to a certain type of move 
                pygame.draw.circle(SCREEN, MOVE_COLOR[symbol], (x+TILE_SIZE//2,y+TILE_SIZE//2), rad)
            
            #if the move was a miss, display the infos of the surrounding tiles (radius 2)
            if symbol == 'M' and game.get_grid_choice() and game.get_hint_choice()<=2:
                
                #display only ships hints
                if game.get_hint_choice() == 0:
                    draw_text(str(player.get_hint_list()[i][0]), x+7, y,size=30,color=L_GREY)
                
                #display only mines hints
                elif game.get_hint_choice() == 1:
                    draw_text("{0:>2}".format(str(player.get_hint_list()[i][1])), x+35, y+32,size=30,color=YELLOW)
                
                #display both
                else:
                    draw_text(str(player.get_hint_list()[i][0]), x+7, y,size=30,color=L_GREY)
                    draw_text("{0:>2}".format(str(player.get_hint_list()[i][1])), x+35, y+32,size=30,color=YELLOW)
                    
            
        
def draw_ships(player, x_offset=0, y_offset=INFO_MARGIN_HEIGHT, sunk_ship=False):
    """draw ships on the screen

    Args:
        player (Player): player whose ships are to be displayed
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
        sunk_ship (bool, optional): only show sunk ships. Defaults to False.
    """
    
    #loop through player's ships
    for ship in player.get_ships():
        
        #skip ships that are not sunk if option is True
        if sunk_ship and not ship.is_sunk():
            continue
        
        #copmute pixel coords
        x = ship.get_x()*TILE_SIZE+INDENT
        y = ship.get_y()*TILE_SIZE+INDENT
        
        #compute width and height of the ship
        if ship.get_orientation() == 'H':
            width = ship.get_size()*TILE_SIZE -2*INDENT
            height = TILE_SIZE -2*INDENT
        else:
            width = TILE_SIZE -2*INDENT
            height = TILE_SIZE*ship.get_size() -2*INDENT
        
        #draw the ship
        rec = pygame.Rect(x+x_offset, y+y_offset, width, height)
        
        #set different colors for normal and sunk ship 
        color = RED if sunk_ship else L_GREY
        
        #display the sip on the screen
        pygame.draw.rect(SCREEN, color , rec, border_radius=50)

def draw_mines(player, x_offset=0, y_offset=INFO_MARGIN_HEIGHT):
    """draw mines on the screen

    Args:
        player (Player): player whose mines are to be displayed
        x_offset (int, optional): horizontal offset. Defaults to 0.
        y_offset (int, optional): vertical offset. Defaults to INFO_MARGIN_HEIGHT.
    """
    
    #loop through all player's mines
    for mine in player.get_mines():
        
        #compute next mine pixel coords
        x = mine.get_x()*TILE_SIZE+TILE_SIZE/2
        y = mine.get_y()*TILE_SIZE+TILE_SIZE/2
        
        #draw a circle corresponding to a mine
        pygame.draw.circle(SCREEN, YELLOW, (x+x_offset,y+y_offset), TILE_SIZE//2-INDENT)

def draw_search_grid(game):
    """display current player searching grid

    Args:
        game (Game): game instance
    """
    #display grid
    draw_grid()
    #display opponent sunk ships
    #draw_ships(game.get_current_opponent(),sunk_ship=True)
    
    #display the moves made by the current player
    draw_shot_fired(game.get_current_player(),game)


def draw_player_grid(game):
    """display current player own grid      

    Args:
        game (Game): game instance
    """
    #display grid
    draw_grid()
    #display player own ships
    draw_ships(game.get_current_player())
    #display player own mines
    draw_mines(game.get_current_player())
    #display the moves made by the opponent
    draw_shot_fired(game.get_current_opponent(),game,search=False)
    
def main_loop():
    """
        Main loop of the game, display the game grid
    """    
    #game initialisation
    game = Game()
    running = True
    played=False
    
    #buttons creation
    buttons = []
    buttons.append(Button("Search grid", 50,game.switch_grid,WIDTH/2,75,(WIDTH/4,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN, text_switch=["Your grid"],colorB=GREEN))
    buttons.append(Button("Ship", 50,game.switch_hint,WIDTH/4,75,(0,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN, text_switch=["Mine","Both","None"],colorB=BLUE))
    buttons.append(Button("Quit", 50,quit,WIDTH/4,75,(3*WIDTH/4,HEIGHT-GRID_SWITCH_MARGIN_HEIGHT+7),SCREEN,colorB=RED))
    
    #main loop
    while running:
        
        victory = game.check_game()
        #handle user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                quit()
            
            #allows you to leave the game by pressing space when the game is over
            if event.type == pygame.KEYDOWN and victory:
                if event.type == pygame.K_SPACE and victory:
                    running=False
                    main_menu()
            
            #get mouse clik
            if event.type == pygame.MOUSEBUTTONDOWN and not victory:
                if pygame.mouse.get_pressed()[0]:
                    
                    #get mouse coords
                    location = pygame.mouse.get_pos()
                    x,y,validity=get_position(location[0], location[1])
                    
                    #check if coords are valid and correspond to a specific tile
                    if validity and game.get_grid_choice():
                        
                        #play or not the player's move depending on whether the same move has already been played
                        played = game.next_move(x,y)
                        
                        #trigger the end of the game
                        if not game.get_current_player().is_alive() or not game.get_current_opponent().is_alive():
                            game.game_over()
                            played = not played
                            
        #fill screen background                  
        SCREEN.fill(GREY)
        
        #allows you to choose between the two display modes
        if game.get_grid_choice():
            draw_search_grid(game)
            
        else:
            draw_player_grid(game)
            
        if victory:
            #display a game over message
            draw_text("Game Over", (1/4)*WIDTH-35, 0,size=80, color=RED)
        else:       
            #display current playe name and health points
            draw_text(game.get_current_player().get_name(), 20, 5,size=70)
            draw_text("{:>2d}HP".format(game.get_current_player().get_hp()[0]), WIDTH-165, 5,size=70,color=game.get_current_player().get_hp()[1])
        
        #display buttons
        buttons_draw(buttons)
        
            
        #update screen
        pygame.display.update()
        mainClock.tick(FPS)
        
        #moves on to the next round
        if played:
            time.sleep(1)
            game.next_round()
            played=False


def help_menu():
    """
        loop and window displaying a visual aid to understand the color code of the game
    """
    
    #buttons creation
    buttons = []
    buttons.append(Button('Main menu', 50,main_menu,525,80,(80,750),SCREEN))
    
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
        pygame.draw.circle(SCREEN, MOVE_COLOR['E'][0], (225,265), 40)
        draw_text('X', 191,210,size=90,color=MOVE_COLOR['E'][1])
        draw_text("Exploded", 320, 235, color=MOVE_COLOR['E'][1])
        
        #hit help
        pygame.draw.circle(SCREEN, MOVE_COLOR['H'], (225,365), 40)
        draw_text("Hit", 320, 335, color=MOVE_COLOR['H'])
        
        #sunk help
        rec2 = pygame.Rect(55, 430 , 3*TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, MOVE_COLOR['S'] , rec2, border_radius=50)
        draw_text("Sunk", 320, 435, color=MOVE_COLOR['S'])
        
        #missed help
        pygame.draw.circle(SCREEN, MOVE_COLOR['M'], (225,565), 40)
        draw_text("Missed", 320, 535, color=MOVE_COLOR['M'])
        
        #show buttons
        buttons_draw(buttons)
        
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)

def comming_soon():
    print("Work in progress")
    
def settings_menu():
    """
        loop and window that allow the user to tweaks the settings of the game
    """
    #creation of the buttons
    buttons = []
    buttons.append(Button('Main menu', 50,main_menu,525,80,(80,750),SCREEN))
    #main loop of the gfunction
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
        
            
        SCREEN.fill(GREY)
        
        #show title
        draw_text( "Settings", 150, 0, size=100, color=BLUE)
        
        draw_text( "Hint radius", 220, 130, size=50, color=BLUE)
        
        #show buttons
        buttons_draw(buttons)
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)


def main_menu():
    """
       loop and window that manage the start menu 
    """
    #creation of the buttons
    buttons = []
    buttons.append(Button('Human Vs Human', 50,main_loop,530,80,(80,450),SCREEN)) 
    buttons.append(Button('Human Vs AI', 50,comming_soon,530,80,(80,550),SCREEN,text_switch=["Work in progress"])) 
    buttons.append(Button('Settings', 50,settings_menu,530,80,(80,650),SCREEN)) 
    buttons.append(Button('Help', 50,help_menu,260,80,(80,750),SCREEN)) 
    buttons.append(Button('Exit', 50,exit,260,80,(350,750),SCREEN)) 
    
    #main loop of the gfunction
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
                
            
        SCREEN.fill(GREY)
        
        #show title
        draw_text( "Battle Ship", 80, HEIGHT/3, size=100, color=BLUE)
        #show logo
        SCREEN.blit(logo, (WIDTH/4,-30))
        #show buttons
        buttons_draw(buttons)
        #update screen
        pygame.display.update()  
        mainClock.tick(FPS)

if __name__ == "__main__":
    main_menu()