import pygame
import sys
from pygame.locals import*
import random
Window_Width = 450
Window_Height = 450
Tiles_row=8
Tiles_col=8
Margin_x=25
Margin_y=25
Tile_size=50
#colours
White = (255,255,255)
Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
def main():
	global Window_Width,Window_Height,Tiles_col,Tiles_row,Margin_y,Margin_x,Tile_size,DisplayScreen
	pygame.display.init()
	DisplayScreen = pygame.display.set_mode((Window_Width,Window_Height))
	DisplayScreen.fill((255,255,255))
	pygame.display.update()
	pygame.display.set_caption("Battleship")
	for i in range(Tiles_row+1):
		pygame.draw.line(DisplayScreen,Black,(Margin_x,Margin_y+i*Tile_size),(Window_Width-Margin_x,Margin_y+i*Tile_size) )
		pygame.display.update()

	for i in range(Tiles_col+1):
		pygame.draw.line(DisplayScreen,Black,(Margin_x+i*Tile_size,Margin_y),(Margin_x+i*Tile_size,Window_Height-Margin_y) )
		pygame.display.update()

	GameLoop()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()


def GameLoop():
	revealed_Tiles = generate_default_tiles(False)
	main_board = generate_default_tiles(None)
	ship_objs = ['Battleship','Cruiser','Destroyer','Submarine']
	main_board = add_ships_to_Board(main_board , ship_objs)
	while True:

		for event in pygame.event.get():
			if event.type == MOUSEMOTION:
				mousex , mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex , mousey = event.pos
				mouse_clicked = True
				tilex ,tiley = get_tile_at_pixel(mousex,mousey)
				if not revealed_Tiles[tilex][tiley] and mouse_clicked:
					revealed_Tiles[tilex][tiley] = True
				if check_revealed_tiles(main_board , [(tilex , tiley)]):
					pygame.draw.rect(DisplayScreen , Blue , (tilex*Tile_size+Margin_x,tiley*Tile_size+Margin_y,Tile_size,Tile_size),4)
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()

def generate_default_tiles(default_value):
	default_tiles = [[default_value]*Tiles_row for i in range(Tiles_col)]
	return default_tiles

def add_ships_to_Board(main_board , ship_objs):
	new_Board = main_board[:]
	ship_length = 0
	for ship in ship_objs:
		valid_shippos = False
		while not valid_shippos:
			xstartpos = random.randint(0,Tiles_row-1)# we have to change	
			ystartpos = random.randint(0,Tiles_col-1)    # this in future'''
			isHorizontal = random.randint(0,1) 

			if 'Battleship' in ship:
				ship_length = 4
			elif 'Cruiser' in ship:
				ship_length = 3
			elif 'Destroyer' in ship:
				ship_length = 2
			elif 'Submarine' in ship:
				ship_length = 1

			valid_shippos, ship_coord = make_ship_position(new_Board , xstartpos , ystartpos, isHorizontal, ship_length, ship)

			if valid_shippos:
				for coord in ship_coord:
					new_Board[coord[0]][coord[1]] = ship
					pygame.draw.rect(DisplayScreen , Red , (coord[0]*Tile_size+Margin_x,coord[1]*Tile_size+Margin_y,Tile_size,Tile_size),4)

	return new_Board

def make_ship_position(new_Board , xstartpos , ystartpos, isHorizontal, ship_length, ship):
	ship_coordinates = []
	if isHorizontal:
		for i in range(ship_length):
			if(i+xstartpos > Tiles_row-1) or (new_Board[i+xstartpos][ystartpos] != None) :
				return (False , ship_coordinates)
			else:
				ship_coordinates.append((i+xstartpos,ystartpos))
	

	if not isHorizontal:
		for i in range(ship_length):
			if(i+ystartpos > Tiles_col-1) or (new_Board[xstartpos][i+ystartpos] != None) :
				return (False , ship_coordinates)
			else:
				ship_coordinates.append((xstartpos,i+ystartpos))
	return (True , ship_coordinates)

def check_revealed_tiles(new_Board , tile):
	print(new_Board[tile[0][0]][tile[0][1]]== None)
	return new_Board[tile[0][0]][tile[0][1]]== None

def get_tile_at_pixel(mousex , mousey):
	left = (int)((mousex - Margin_x)/Tile_size)
	top = (int)((mousey - Margin_y)/Tile_size)
	#tile_rect = pygame.Rect(left , top , Tile_size , Tile_size)
	return (left , top)


if __name__ == "__main__":
	main()
