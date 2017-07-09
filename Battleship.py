import pygame
import sys
from pygame.locals import*
import random
import time
pygame.init()
Window_Width = 800
Window_Height = 800
Tiles_row=10
Tiles_col=10
Margin_x=25
Margin_y=25
Tile_size=40
Explosionspeed = 10
White = (255,255,255)
Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
smallfont = pygame.font.SysFont("comicsansms",20)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",70)
def main():
	
	global Window_Width,Window_Height,Tiles_col,Tiles_row,Margin_y,Margin_x,Tile_size,DisplayScreen,EXPLOSION_IMAGES,FPSCLOCK,MISSIMAGES
	pygame.mixer.pre_init(44100,16,2,4096)
	pygame.display.init()
	FPSCLOCK=pygame.time.Clock()

	DisplayScreen = pygame.display.set_mode((Window_Width,Window_Height))
	
	DisplayScreen.fill((255,255,255))
	
	MISSIMAGES = [ pygame.image.load("images/thumbsdown1.png"), pygame.image.load("images/thumbsdown2.png"),
        pygame.image.load("images/thumbsdown.png"),pygame.image.load("images/final.png")]
	EXPLOSION_IMAGES = [
        pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
        pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
        pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]
	pygame.display.update()
	pygame.display.set_caption("Battleship")
	
	GameLoop()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

def manualplayer(board):
	Total_shot_list=[]
	BlastSound = pygame.mixer.Sound("blast.wav")
	MissSound = pygame.mixer.Sound("miss.wav")
	Destroy=0
	shots=0
	while True:
		tilex=None
		for event in pygame.event.get():

			if event.type==MOUSEBUTTONUP:
				typemessage("")
				mousex,mousey= event.pos
				tilex,tiley=get_tile_at_pixel(mousex,mousey)
				if tilex==None and tiley==None:
					continue
				elif (tilex,tiley) in Total_shot_list:
					typemessage("Invalid Choice")
					continue
				elif board[tilex][tiley]==None:
					shots+=1
					Total_shot_list.append((tilex,tiley))
					makesound(MissSound)
					blowup_missanimation((tilex,tiley))

				elif board[tilex][tiley] is not None:
					shots+=1
					Destroy+=1
					Total_shot_list.append((tilex,tiley))
					makesound(BlastSound)
					blowup_animation((tilex,tiley))
					if Destroy>13:
						typemessage("You Win")
						return shots
					if check_Destroy(board,(tilex,tiley),Total_shot_list):
						typemessage("DESTROYED")
			elif event.type==QUIT:
				pygame.quit()
				sys.exit()


			if shots==Tiles_row*Tiles_col:
				typemessage("Game Over")
				return shots
		
def placeship(revealed_Tiles,main_board,ship_objs):
	mousex=0
	mousey=0
	for ship in ship_objs:
		if ship=="Battleship":
			typemessage("Click on the start and last box for length of ship=4 ")
			length=4
			valid=False
			while not valid:
				while True:
					tilex=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex,tiley=get_tile_at_pixel(mousex,mousey)
							if tilex==None and tiley==None:
								continue
							elif main_board[tilex][tiley]==None:
								#main_board[tilex][tiley]=ship
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex!=None:
						break
				
				while True:
					tilex2=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex2,tiley2=get_tile_at_pixel(mousex,mousey)
							if tilex2==None and tiley2==None:
								continue
							elif main_board[tilex2][tiley2]==None:
								#main_board[tilex2][tiley2]=ship
								break
				
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex2!=None:
						break
				flag=0
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							if main_board[tilex][i]!=None:
								flag=1
								break
					else:
						for i in range(tiley2,tiley2+length):
							if main_board[tilex][i]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				flag=0
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break
					else:
						for i in range(tilex2,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					typemessage("")
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					else:
						for i in range(tiley2,tiley2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					valid=True
					break
				
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					typemessage("")
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley]=ship
					else:
						for i in range(tilex2,tilex2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley2*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley2]=ship
					valid=True
					break
				typemessage("invalid move")
			
		elif ship=="Destroyer":

			typemessage("Click on the start and last box for length of ship=2 ")
			length=2
			valid=False
			while not valid:
				while True:
					tilex=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex,tiley=get_tile_at_pixel(mousex,mousey)
							if tilex==None and tiley==None:
								continue
							elif main_board[tilex][tiley]==None:
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex!=None:
						break
				
				while True:
					tilex2=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex2,tiley2=get_tile_at_pixel(mousex,mousey)
							if tilex2==None and tiley2==None:
								continue
							elif main_board[tilex2][tiley2]==None:
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex2!=None:
						break

				flag=0
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							if main_board[tilex][i]!=None:
								flag=1
								break
					else:
						for i in range(tiley2,tiley2+length):
							if main_board[tilex][i]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				flag=0
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break
					else:
						for i in range(tilex2,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					typemessage("")
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					else:
						for i in range(tiley2,tiley2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					valid=True
					break
				
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					typemessage("")
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley]=ship
					else:
						for i in range(tilex2,tilex2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley2*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley2]=ship
					valid=True
					break
				typemessage("invalid move")


		elif ship=="Cruiser": 
			typemessage("Click on the start and last box for length of ship=3 ")
			length=3
			valid=False
			while not valid:
				while True:
					tilex=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex,tiley=get_tile_at_pixel(mousex,mousey)
							if tilex==None and tiley==None:
								continue
							elif main_board[tilex][tiley]==None:
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex!=None:
						break
				

				while True:
						tilex2=None
						for event in pygame.event.get():
							if event.type==MOUSEBUTTONUP:
								mousex,mousey= event.pos
								tilex2,tiley2=get_tile_at_pixel(mousex,mousey)
								if tilex2==None and tiley2==None:
									continue
								elif main_board[tilex2][tiley2]==None:
									break
							elif event.type==QUIT:
								pygame.quit()
								sys.exit()

						if tilex2!=None:
							break
				
					
				flag=0
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							if main_board[tilex][i]!=None:
								flag=1
								break
					else:
						for i in range(tiley2,tiley2+length):
							if main_board[tilex][i]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				flag=0
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break
					else:
						for i in range(tilex2,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue


				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					typemessage("")
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					else:
						for i in range(tiley2,tiley2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					valid=True
					break
				
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					typemessage("")
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley]=ship
					else:
						for i in range(tilex2,tilex2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley2*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley2]=ship
					valid=True
					break
				typemessage("invalid move")


		elif ship=="Submarine":

			typemessage("Click on the start and last box for length of ship=5 ")
			length=5
			valid=False
			while not valid:
				while True:
					tilex=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex,tiley=get_tile_at_pixel(mousex,mousey)
							if tilex==None and tiley==None:
								continue
							elif main_board[tilex][tiley]==None:
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex!=None:
						break
				
				while True:
					tilex2=None
					for event in pygame.event.get():
						if event.type==MOUSEBUTTONUP:
							mousex,mousey= event.pos
							tilex2,tiley2=get_tile_at_pixel(mousex,mousey)
							if tilex2==None and tiley2==None:
								continue
							elif main_board[tilex2][tiley2]==None:
								break
						elif event.type==QUIT:
							pygame.quit()
							sys.exit()

					if tilex2!=None:
						break

				flag=0
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							if main_board[tilex][i]!=None:
								flag=1
								break
					else:
						for i in range(tiley2,tiley2+length):
							if main_board[tilex][i]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				flag=0
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break
					else:
						for i in range(tilex2,tilex+length):
							if main_board[i][tiley]!=None:
								flag=1
								break

				if flag==1:
					typemessage("Invalid move")
					continue

				
				if tilex==tilex2 and (tiley-tiley2==length-1 or tiley2-tiley==length-1):
					typemessage("")
					if tiley<tiley2:
						for i in range(tiley,tiley+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					else:
						for i in range(tiley2,tiley2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (tilex*Tile_size+Margin_x,i*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[tilex][i]=ship
					valid=True
					break
				
				if tiley==tiley2 and (tilex-tilex2==length-1 or tilex2-tilex==length-1):
					typemessage("")
					if tilex<tilex2:
						for i in range(tilex,tilex+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley]=ship
					else:
						for i in range(tilex2,tilex2+length):
							pygame.draw.rect(DisplayScreen , (0,0,255) , (i*Tile_size+Margin_x,tiley2*Tile_size+Margin_y,Tile_size,Tile_size),4)
							pygame.display.update()
							main_board[i][tiley2]=ship
					valid=True
					break
				typemessage("invalid move")

	return main_board
	

def GameLoop():

	string=game_intro()
	board=[]
	play = pygame.image.load("play.png")
	play = pygame.transform.scale(play , (Window_Width,Window_Height))
	DisplayScreen.blit(play,(0,0))
	pygame.display.update()
	for i in range(Tiles_row+1):
		pygame.draw.line(DisplayScreen,Black,(Margin_x,Margin_y+i*Tile_size),(Margin_x+Tiles_row*Tile_size,Margin_y+i*Tile_size) )
		pygame.display.update()

	for i in range(Tiles_col+1):
		pygame.draw.line(DisplayScreen,Black,(Margin_x+i*Tile_size,Margin_y),(Margin_x+i*Tile_size,Margin_y+Tile_size*Tiles_col) )
		pygame.display.update()
	
	
	revealed_Tiles = generate_default_tiles(False)
	main_board = generate_default_tiles(None)
	ship_objs = ['Battleship','Cruiser','Destroyer','Submarine']
	
	if string=="ship":
		main_board=placeship(revealed_Tiles,main_board,ship_objs)
		shots=real_game(main_board)
	
	elif string=="watch":
		main_board = add_ships_to_Board(main_board , ship_objs)
		shots=real_game(main_board)
	
	elif string=="easy":
		board=easyGamelevel()
		typemessage("Destroy 4 ships consisting of length 2,3,4,5")
		time.sleep(.5)
		shots=manualplayer(board)
		
	elif string=="hard":
		board=hardgamelevel()
		typemessage("Destroy 4 ships consisting of length 2,3,4,5")
		time.sleep(.5)
		shots=manualplayer(board)
		
	exit_screen(str(shots))
	

def generate_default_tiles(default_value):
	default_tiles = [[default_value]*Tiles_row for i in range(Tiles_col)]
	return default_tiles

def left_top_coord_tile(tilex ,tiley):
	left = tilex*Tile_size + Margin_x
	top = tiley*Tile_size + Margin_y
	return(left,top)

def add_ships_to_Board(main_board , ship_objs):
	new_Board = main_board[:]
	ship_length = 0
	for ship in ship_objs:
		valid_shippos = False
		while not valid_shippos:
			xstartpos = random.randint(0,Tiles_row-1)	
			ystartpos = random.randint(0,Tiles_col-1)    
			isHorizontal = random.randint(0,1) 

			if 'Battleship' in ship:
				ship_length = 4
			elif 'Cruiser' in ship:
				ship_length = 3
			elif 'Destroyer' in ship:
				ship_length = 2
			elif 'Submarine' in ship:
				ship_length = 5

			valid_shippos, ship_coord = make_ship_position(new_Board , xstartpos , ystartpos, isHorizontal, ship_length, ship)

			if valid_shippos:
				if ship=="Battleship":
					for coord in ship_coord:
						new_Board[coord[0]][coord[1]] = ship
						pygame.draw.rect(DisplayScreen , Red , (coord[0]*Tile_size+Margin_x,coord[1]*Tile_size+Margin_y,Tile_size,Tile_size),4)
				elif ship=="Cruiser":
					for coord in ship_coord:
						new_Board[coord[0]][coord[1]] = ship
						pygame.draw.rect(DisplayScreen , Blue , (coord[0]*Tile_size+Margin_x,coord[1]*Tile_size+Margin_y,Tile_size,Tile_size),4)
				elif ship=="Destroyer":
					for coord in ship_coord:
						new_Board[coord[0]][coord[1]] = ship
						pygame.draw.rect(DisplayScreen , (0,255,0) , (coord[0]*Tile_size+Margin_x,coord[1]*Tile_size+Margin_y,Tile_size,Tile_size),4)
				elif ship=="Submarine":
					for coord in ship_coord:
						new_Board[coord[0]][coord[1]] = ship
						pygame.draw.rect(DisplayScreen , (255,0,255) , (coord[0]*Tile_size+Margin_x,coord[1]*Tile_size+Margin_y,Tile_size,Tile_size),4)

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
	return new_Board[tile[0][0]][tile[0][1]]== None

def get_tile_at_pixel(mousex , mousey):
	left = (int)((mousex - Margin_x)/Tile_size)
	top = (int)((mousey - Margin_y)/Tile_size)
	if left<Tiles_row and top< Tiles_col:
		return (left , top)
	return (None,None)

def probability(shots):
	board=[]
	MISS=-1

	board = [[0]*Tiles_row for i in range(Tiles_col)]

	for (x,y) in shots:
		board[x][y]=MISS
	
	for k in range(1,5):
		length=k+1
		for i in range(Tiles_row):
			for j in range(Tiles_col):
				flag=0
				for l in range(j,j+length):
					if j+length-1>=Tiles_col:
						flag=1
						break

					if (i,l) in shots:
						flag=1
						break
				if flag is 0:
					for l in range(j,j+length):
						board[i][l]+=1

	for k in range(1,5):
		length=k+1
		for i in range(Tiles_row):
			for j in range(Tiles_col):
				flag=0
				for l in range(i,i+length):
					if i+length-1>=Tiles_row:
						flag=1
						break

					if (l,j) in shots:
						flag=1
						break
				if flag is 0:
					for l in range(i,i+length):
						board[l][j]+=1

	
	return (max_probability(board),shots)


def max_probability(board):
	maximum=0
	index=[]
	for i in range(Tiles_row):
		for j in range(Tiles_col):
			if board[i][j] > maximum:
				maximum=board[i][j]
				index=[]
				index.append((i,j))
			elif board[i][j] == maximum:
				index=[]
				index.append((i,j))

	return random.choice(index)
		
def adjacent(main_board,shot_pos,Total_shot_list,shots,DESTROY,MissSound,BlastSound):
	k=1
	i=shot_pos[0]
	j=shot_pos[1]

	if check_Destroy(main_board,(i,j),Total_shot_list):
		typemessage("DESTROYED")
		time.sleep(.5)
		typemessage("")
		return (shots,DESTROY,Total_shot_list)
	while True:
		if k+i<Tiles_row :
			if (i+k,j) in Total_shot_list:
				break
			if main_board[k+i][j] is None:
				shots+=1
				Total_shot_list.append((k+i,j))
				makesound(MissSound)
				blowup_missanimation((k+i,j))
				break 
			makesound(BlastSound)
			blowup_animation((k+i,j))
			k+=1
			DESTROY+=1
			Total_shot_list.append((k+i-1,j))
			if check_Destroy(main_board,(i,j),Total_shot_list):
				typemessage("DESTROYED")
				time.sleep(.5)
				typemessage("")
				return (shots,DESTROY,Total_shot_list)

			shots+=1
			if DESTROY>13:
				return (shots,DESTROY,Total_shot_list)
			
		else: 
			break

	k=1
	
	while True:
		if i-k>=0:
			if (i-k,j) in Total_shot_list:
				break
			if main_board[i-k][j] is None:
				shots+=1
				Total_shot_list.append((i-k,j))
				makesound(MissSound)
				blowup_missanimation((i-k,j))
				break 
			makesound(BlastSound)
			blowup_animation((i-k,j))
			k+=1
			DESTROY+=1
			Total_shot_list.append((i+1-k,j))
			if check_Destroy(main_board,(i,j),Total_shot_list):
				typemessage("DESTROYED")
				time.sleep(.5)
				typemessage("")
				return (shots,DESTROY,Total_shot_list)
			shots+=1
			if DESTROY>13:
				return (shots,DESTROY,Total_shot_list)
		else:
			break

	k=1
	
	while True:
		if k+j<Tiles_col:
			if (i,j+k) in Total_shot_list:
				break
			if main_board[i][j+k] is None:
				shots+=1
				Total_shot_list.append((i,j+k))
				makesound(MissSound)
				blowup_missanimation((i,j+k))
				break 
			makesound(BlastSound)
			blowup_animation((i,j+k))
			k+=1
			DESTROY+=1
			Total_shot_list.append((i,k-1+j))
			if check_Destroy(main_board,(i,j),Total_shot_list):
				typemessage("DESTROYED")
				time.sleep(.5)
				typemessage("")
				return (shots,DESTROY,Total_shot_list)
			shots+=1
			if DESTROY>13:
				return (shots,DESTROY,Total_shot_list)
		else:
			break

	k=1
	
	while True:
		if j>=k:
			if (i,j-k) in Total_shot_list:
				break
			if main_board[i][j-k] is None:
				shots+=1
				Total_shot_list.append((i,j-k))
				makesound(MissSound)
				blowup_missanimation((i,j-k))
				break 
			makesound(BlastSound)
			blowup_animation((i,j-k))
			k+=1
			DESTROY+=1
			Total_shot_list.append((i,j-k+1))
			if check_Destroy(main_board,(i,j),Total_shot_list):
				typemessage("DESTROYED")
				time.sleep(.5)
				typemessage("")
				return (shots,DESTROY,Total_shot_list)
			shots+=1
			if DESTROY>13:
				return (shots,DESTROY,Total_shot_list)
		else:
			break
	return (shots,DESTROY,Total_shot_list)

def real_game(main_board):
	corners = [(0,0),(0,Tiles_col-1),(Tiles_row-1,0),(Tiles_row-1,Tiles_col-1)]
	BlastSound = pygame.mixer.Sound("blast.wav")
	MissSound = pygame.mixer.Sound("miss.wav")
	Total_shot_list=[]
	DESTROY=0
	shots=0
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		(i,j),Total_shot_list=probability(Total_shot_list)
		if shots !=0 and shots%17==0:
			pos=random.randint(0,3)
			if corners[pos] not in Total_shot_list:
				(i,j)=corners[pos]

		Total_shot_list.append((i,j))
		if main_board[i][j] is not None:
			shots+=1
			DESTROY+=1
			blowup_animation((i,j))
			makesound(BlastSound)
			if DESTROY>13:
				break
			
			shots,DESTROY,Total_shot_list= adjacent(main_board,(i,j),Total_shot_list,shots,DESTROY,MissSound,BlastSound)
		else:
			shots+=1
			makesound(MissSound)
			blowup_missanimation((i,j))
		if DESTROY>13:
			break
	return shots

def typemessage(text):
	DisplayScreen.fill(White, rect=(25,450,700,100))
	pygame.display.update()
	msgtoscreen(text,Red,100,"small",325)
	pygame.display.update()

def check_Destroy(main_board,coordi,Total_shot_list):
	i=coordi[0]
	j=coordi[1]
	ship=main_board[i][j]
	k=i
	l=j
	while (k-1>=0 and main_board[k-1][l] == ship):
		if (k-1,l) not in Total_shot_list:
			return False
		else:
			k-=1

	k=i
	l=j

	while (k+1<Tiles_row and main_board[k+1][l] == ship):
		if (k+1,l) not in Total_shot_list:
			return False
		else:
			k+=1

	k=i
	l=j

	while (l-1>=0 and main_board[k][l-1] == ship):
		if (k,l-1) not in Total_shot_list:
			return False
		else:
			l-=1

	k=i
	l=j

	while (l+1<Tiles_col and main_board[k][l+1] == ship):
		if (k,l+1) not in Total_shot_list:
			return False
		else:
			l+=1

	k=i
	l=j

	return True

def blowup_animation(coordi):
	for image in EXPLOSION_IMAGES:
		image = pygame.transform.scale(image , (Tile_size,Tile_size))
		DisplayScreen.blit(image,(coordi[0]*Tile_size+Margin_x,coordi[1]*Tile_size+Margin_y))
		pygame.display.flip()
		FPSCLOCK.tick(Explosionspeed)

def blowup_missanimation(coordi):
	for image in MISSIMAGES:
		image=pygame.transform.scale(image , (Tile_size,Tile_size))
		DisplayScreen.blit(image,(coordi[0]*Tile_size+Margin_x,coordi[1]*Tile_size+Margin_y))
		pygame.display.flip()
		FPSCLOCK.tick(Explosionspeed)

def makesound(sound):
	pygame.mixer.Sound.play(sound)

def game_intro():
	front = pygame.image.load("front.png")
	front = pygame.transform.scale(front,(Window_Width,Window_Height))
	DisplayScreen.blit(front,(0,0))
	pygame.display.update()
	intro=True
	while intro:
		msgtoscreen("PRESS E TO PLAY EASY MANUALLY",(230,230,230),160,"small")
		msgtoscreen("PRESS H TO PLAY HARD MANUALLY",(230,230,230),190,"small")
		msgtoscreen("PRESS S TO PLACE SHIPS FOR AI",(230,230,230),130,"small")
		msgtoscreen("PRESS W TO WATCH AI PLAY",(230,230,230),100,"small")
		msgtoscreen("PRESS Q TO QUIT",(230,230,230),70,"small")
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_e:
					intro = False
					return "easy"
				elif event.key == pygame.K_h:
					intro = False
					return "hard"
				elif event.key == pygame.K_s:
					intro=False
					return "ship"
				elif event.key == pygame.K_w:
					intro=False
					return "watch"
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

def exit_screen(shots):
	front = pygame.image.load("end.png")
	front = pygame.transform.scale(front,(Window_Width,Window_Height))
	DisplayScreen.blit(front,(0,0))
	pygame.display.update()
	intro=True
	while intro:
		msgtoscreen("PRESS R TO PLAY AGAIN OR Q TO EXIT",(190,190,190),-120,"small")
		msgtoscreen("Total  shots= " + shots,(210,210,210),-90,"small")
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					intro = False
					DisplayScreen.fill(White)
					pygame.display.update()
					GameLoop()
				if event.key == pygame.K_q:
					pygame.quit()
					quit()


def text_objects(msg,color,size):
	if size=="small":
		Textsurf = smallfont.render(msg,True,color)
	elif size=="med":
		Textsurf = medfont.render(msg,True,color)
	elif size=="large":
		Textsurf = largefont.render(msg,True,color)
		
	return Textsurf,Textsurf.get_rect()

def msgtoscreen(text,color,y_displace=0,size="small",x_displace=Window_Width/2):
	Textsurf,TextRect = text_objects(text,color,size)
	TextRect.center= x_displace , Window_Height/2+y_displace
	DisplayScreen.blit(Textsurf,TextRect)

def easyGamelevel():
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Battleship', None, None, None, None], [None, None, None, None, None, 'Battleship', None, None, None, None], [None, None, None, None, None, 'Battleship', None, None, 'Cruiser', None], [None, None, None, None, None, 'Battleship', None, None, 'Cruiser', None], [None, 'Submarine', None, None, None, None, None, None, 'Cruiser', None], [None, 'Submarine', None, None, None, None, None, None, None, None], [None, 'Submarine', None, None, None, None, None, None, 'Destroyer', None], [None, 'Submarine', None, None, None, None, None, None, 'Destroyer', None], [None, 'Submarine', None, None, None, None, None, None, None, None]]
	easy=[]
	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Submarine', None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser'], [None, None, 'Submarine', None, None, None, None, None, None, None], [None, None, 'Submarine', None, None, None, None, None, None, None], [None, None, 'Submarine', None, 'Battleship', None, None, None, None, None], [None, None, 'Submarine', None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, 'Destroyer', None, None], [None, None, None, None, None, None, None, 'Destroyer', None, None]]
	easy.append(level)
	level=[]
	level=[[None, None, None, None, 'Cruiser', None, None, None, None, None], [None, None, None, None, 'Cruiser', None, None, None, None, None], [None, None, None, None, 'Cruiser', None, None, None, 'Submarine', None], [None, None, None, None, None, None, None, None, 'Submarine', None], [None, None, None, None, None, None, None, None, 'Submarine', None], [None, 'Battleship', None, None, None, None, None, None, 'Submarine', None], [None, 'Battleship', None, None, None, None, None, None, 'Submarine', None], [None, 'Battleship', None, None, None, None, None, None, None, None], [None, 'Battleship', None, 'Destroyer', 'Destroyer', None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]
	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, None, None, None], ['Submarine', None, None, None, 'Battleship', None, None, None, None, None], ['Submarine', None, None, None, 'Battleship', None, None, None, None, None], ['Submarine', None, None, None, None, None, 'Destroyer', 'Destroyer', None, None], ['Submarine', None, None, None, None, None, None, None, None, None], ['Submarine', None, None, None, None, None, None, None, None, None]]
	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Submarine', None, None, None, None], [None, None, 'Cruiser', None, None, 'Submarine', None, 'Battleship', None, None], [None, None, 'Cruiser', None, None, 'Submarine', None, 'Battleship', None, None], [None, None, 'Cruiser', None, None, 'Submarine', None, 'Battleship', None, None], [None, None, None, 'Destroyer', None, 'Submarine', None, 'Battleship', None, None], [None, None, None, 'Destroyer', None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Cruiser', None, None, None, None, None, None, None], [None, None, 'Cruiser', None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None], [None, None, 'Cruiser', None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Destroyer', 'Destroyer', None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, 'Destroyer', 'Destroyer', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, 'Cruiser', None, None, None, None, None], [None, None, None, None, 'Cruiser', None, 'Battleship', 'Battleship', 'Battleship', 'Battleship'], [None, None, None, None, 'Cruiser', None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Destroyer', 'Destroyer', None, None, None, None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, 'Battleship', 'Cruiser', 'Submarine', None, None], [None, None, None, None, None, 'Battleship', 'Cruiser', 'Submarine', None, None], [None, None, None, None, None, 'Battleship', 'Cruiser', 'Submarine', None, None], [None, None, None, None, None, 'Battleship', None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Battleship', None, 'Cruiser', None, None, None, None, 'Destroyer', 'Destroyer', None], ['Battleship', None, 'Cruiser', None, None, None, None, None, None, None], ['Battleship', None, 'Cruiser', None, None, None, None, None, None, None], ['Battleship', None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, 'Destroyer', None, None, None], [None, None, None, None, None, None, 'Destroyer', None, None, None], [None, None, None, None, 'Submarine', None, None, None, None, None], [None, None, None, None, 'Submarine', None, None, None, None, None], [None, None, None, None, 'Submarine', None, None, None, None, None], ['Cruiser', None, None, None, 'Submarine', None, None, None, None, None], ['Cruiser', None, None, None, 'Submarine', None, None, None, None, None], ['Cruiser', None, None, None, None, None, None, None, None, None], [None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, 'Destroyer', None, None, None, None, None, None, None, None], [None, 'Destroyer', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 'Battleship', None], [None, None, None, None, 'Cruiser', None, None, 'Submarine', 'Battleship', None], [None, None, None, None, 'Cruiser', None, None, 'Submarine', 'Battleship', None], [None, None, None, None, 'Cruiser', None, None, 'Submarine', 'Battleship', None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, None, None, None], [None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None], [None, None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, 'Destroyer', None, None, 'Cruiser', None, None, None], [None, None, None, 'Destroyer', None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, 'Destroyer', 'Destroyer', None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None, None], [None, None, None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None], [None, None, None, 'Submarine', None, None, None, None, None, None], [None, None, None, 'Submarine', None, None, None, None, None, 'Battleship'], [None, None, None, 'Submarine', None, None, None, None, None, 'Battleship'], [None, None, None, 'Submarine', None, None, None, None, None, 'Battleship'], [None, None, None, 'Submarine', None, None, None, None, None, 'Battleship'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, 'Destroyer', 'Destroyer', None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Submarine', None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser'], [None, None, 'Submarine', None, None, None, None, None, None, None], [None, None, 'Submarine', None, None, None, None, None, None, None], [None, None, 'Submarine', None, 'Battleship', None, None, None, None, None], [None, None, 'Submarine', None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, 'Destroyer', None, None], [None, None, None, None, None, None, None, 'Destroyer', None, None]]

	easy.append(level)
	level=[]
	level=[['Submarine', None, None, None, None, None, None, 'Battleship', None, None], ['Submarine', None, None, None, None, None, None, 'Battleship', None, None], ['Submarine', None, None, None, None, None, 'Cruiser', 'Battleship', None, None], ['Submarine', None, None, None, None, None, 'Cruiser', 'Battleship', None, None], ['Submarine', None, None, None, None, None, 'Cruiser', None, None, None], [None, None, None, None, None, 'Destroyer', 'Destroyer', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Submarine', None, None, None, None, None, None, None, None, 'Destroyer'], ['Submarine', None, None, None, None, None, None, None, None, 'Destroyer'], ['Submarine', None, None, None, None, None, None, None, None, None], ['Submarine', None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None], ['Submarine', None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, 'Destroyer', 'Destroyer', None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None]]

	easy.append(level)
	level=[]
	level=[['Cruiser', None, None, None, None, None, None, None, None, None], ['Cruiser', None, None, None, None, None, None, None, None, None], ['Cruiser', None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, None, None, None, None, None, 'Submarine', None, None, None], [None, 'Battleship', None, None, None, None, 'Submarine', None, None, None], [None, 'Battleship', None, None, None, None, None, None, None, 'Destroyer'], [None, 'Battleship', None, None, None, None, None, None, None, 'Destroyer'], [None, 'Battleship', None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, 'Battleship'], ['Cruiser', None, None, None, None, None, None, None, None, 'Battleship'], ['Cruiser', None, None, None, None, None, None, None, None, 'Battleship'], ['Cruiser', None, None, None, None, None, None, None, None, 'Battleship'], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, 'Destroyer', 'Destroyer', None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Destroyer', None, None, 'Submarine'], [None, None, None, None, None, None, 'Destroyer', None, None, 'Submarine'], [None, None, None, None, None, None, None, None, None, 'Submarine'], [None, None, None, None, 'Battleship', None, None, None, None, 'Submarine'], [None, None, None, None, 'Battleship', None, None, None, None, 'Submarine'], [None, None, None, None, 'Battleship', None, None, None, None, None], [None, None, None, None, 'Battleship', None, None, 'Cruiser', 'Cruiser', 'Cruiser'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Destroyer', None, None, None], [None, None, None, None, None, None, 'Destroyer', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine'], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship'], [None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser'], [None, None, 'Destroyer', None, None, None, None, None, None, None], [None, None, 'Destroyer', None, None, None, None, None, None, None]]

	easy.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Destroyer', None, None, None, None, None, None, None, None, None], ['Destroyer', None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None], [None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	easy.append(level)
	return assign_ship(easy)

def hardgamelevel():
	hard=[]
	level=[]
	level=[[None, None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Destroyer', None, None, None, None, None, None], [None, None, None, 'Destroyer', None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None], [None, None, None, None, None, 'Submarine', None, None, None, None], [None, None, None, None, None, 'Submarine', None, None, None, None], [None, None, None, None, None, 'Submarine', None, None, None, None], [None, None, None, None, None, 'Submarine', None, 'Destroyer', 'Destroyer', None], [None, None, None, None, None, 'Submarine', None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, 'Battleship'], [None, 'Cruiser', None, None, None, 'Destroyer', None, None, None, 'Battleship'], [None, 'Cruiser', None, None, None, 'Destroyer', None, None, None, 'Battleship'], [None, 'Cruiser', None, None, None, None, None, None, None, 'Battleship'], [None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 'Cruiser', None], [None, None, None, None, None, None, None, None, 'Cruiser', None], [None, None, None, None, None, None, None, None, 'Cruiser', None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Destroyer', 'Destroyer', None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, 'Submarine'], [None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, 'Submarine'], [None, None, None, None, 'Destroyer', 'Destroyer', None, None, None, 'Submarine'], [None, None, None, None, None, None, None, None, None, 'Submarine'], [None, None, None, None, None, None, None, None, None, 'Submarine'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Cruiser', None, None, None, None, None, None], [None, None, None, 'Cruiser', None, None, None, None, None, None], [None, None, None, 'Cruiser', None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None, None], [None, None, None, None, None, None, 'Destroyer', 'Destroyer', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None], [None, None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, None, None, None, None, None], ['Battleship', None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None], [None, None, None, None, None, None, 'Destroyer', 'Destroyer', None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, 'Destroyer'], [None, None, None, None, None, None, None, None, None, 'Destroyer'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Cruiser', None, None, None, None], ['Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Cruiser', None, None, None, None], [None, None, None, None, None, 'Cruiser', None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None], [None, None, None, None, 'Destroyer', 'Destroyer', None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Battleship', None, None, None, None, None, None], [None, None, None, 'Battleship', None, None, None, None, None, None], [None, None, None, 'Battleship', None, None, None, None, None, None], [None, None, None, 'Battleship', None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None], [None, None, 'Destroyer', 'Destroyer', None, None, None, None, None, None], [None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, 'Submarine', 'Battleship', None, None, None, None, None, None, None], [None, 'Submarine', 'Battleship', None, None, None, None, None, None, None], [None, 'Submarine', 'Battleship', None, None, None, None, None, None, None], [None, 'Submarine', 'Battleship', None, None, None, None, None, None, None], [None, 'Submarine', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, 'Destroyer'], [None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, 'Destroyer'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Destroyer', None, None, None, None, None, None, None, 'Submarine', None], ['Destroyer', None, None, None, None, None, None, None, 'Submarine', None], [None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, 'Submarine', None], [None, None, None, None, None, None, None, None, 'Submarine', None], [None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, 'Submarine', None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, 'Cruiser', 'Cruiser', 'Cruiser'], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, None, 'Submarine', None, None], [None, None, None, None, None, None, 'Destroyer', 'Submarine', None, None], [None, None, None, None, None, None, 'Destroyer', 'Submarine', None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Destroyer', 'Destroyer', None, None, None], [None, None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None], ['Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine', None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	level=[]
	level=[[None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, 'Cruiser', 'Cruiser', 'Cruiser', None, None, None, None, None], [None, None, 'Battleship', 'Battleship', 'Battleship', 'Battleship', None, None, None, None], [None, None, None, None, None, None, None, None, None, None], ['Destroyer', None, None, None, None, None, None, None, None, None], ['Destroyer', None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, 'Submarine', 'Submarine', 'Submarine', 'Submarine', 'Submarine'], [None, None, None, None, None, None, None, None, None, None]]

	hard.append(level)
	return assign_ship(hard)

def assign_ship(easy):
	pos = random.randint(0,len(easy)-1)
	board= easy[pos]
	'''for i in range(Tiles_row):
		for j in range(Tiles_col):
			if board[i][j]=="Battleship":
				pygame.draw.rect(DisplayScreen , Red , (i*Tile_size+Margin_x,j*Tile_size+Margin_y,Tile_size,Tile_size),4)
				pygame.display.update()
			elif board[i][j]=="Cruiser":
				pygame.draw.rect(DisplayScreen , Blue , (i*Tile_size+Margin_x,j*Tile_size+Margin_y,Tile_size,Tile_size),4)
				pygame.display.update()
			elif board[i][j]=="Destroyer":
				pygame.draw.rect(DisplayScreen , (0,255,0) , (i*Tile_size+Margin_x,j*Tile_size+Margin_y,Tile_size,Tile_size),4)
				pygame.display.update()
			elif board[i][j]=="Submarine":
				pygame.draw.rect(DisplayScreen , (255,0,255) , (i*Tile_size+Margin_x,j*Tile_size+Margin_y,Tile_size,Tile_size),4)
				pygame.display.update()'''
	return board



if __name__ == "__main__":
	main()