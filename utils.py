#Colors
GREY = (40,50,60)
L_GREY = (211, 211, 211)
WHITE = (255,255,255) 
BLUE = (14,101,229)
RED = (255,0,0)
BLACK = (0,0,0)
ORANGE = (250,140,20)
GREEN = (50,200,150)
PURPLE = (150, 111, 214)
YELLOW = (255,233,0)

#colors corresponding to each move
MOVE_COLOR={'M':BLUE,'H':ORANGE,'S':RED,'E':[YELLOW,BLACK]}

#color corresponding to each starting elements
ELEMENT_COLOR={"Ship":L_GREY,"Mine":YELLOW}

#tiles
TILE_SIZE = 70
NB_TILE = 10

#other screen element size
INFO_MARGIN_HEIGHT = 100
GRID_SWITCH_MARGIN_HEIGHT = 85
INDENT = 15


FPS = 30

#screen dimension
WIDTH = TILE_SIZE*NB_TILE
HEIGHT = TILE_SIZE*NB_TILE+INFO_MARGIN_HEIGHT+GRID_SWITCH_MARGIN_HEIGHT

def get_index(x,y):
    """compute the index from x and y coords

    Args:
        x (int): horizontal coord
        y (int): vertical coords

    Returns:
        int: index
    """
    return y*NB_TILE+x

def get_coords(idx):
    """compute the x and y coords from an index

    Args:
        idx (int): index

    Returns:
        (int,int): (x,y) x coord and y coords
    """
    return idx%10,idx//10

def get_position(x,y):
    """compute the corresponding coords in the grid of the mouse coords

    Args:
        x (int): horizontal coords
        y (int): vertical coords

    Returns:
        (int,int,bool): x coords scaled to TILE_SIZE
                        y coords scaled to TILE_SIZE
                        position returned is in the grid
    """
    #compute grid coordinates
    a=x//TILE_SIZE
    b=(y-INFO_MARGIN_HEIGHT)//TILE_SIZE
    validity=False
    #check if grid coords are valide 
    if 0<=a<NB_TILE and 0<=b<NB_TILE:
        validity=True
    return a,b,validity

def useless():
    """useless func, used when a callable is needed but we don't want anything to be done
    """
    pass