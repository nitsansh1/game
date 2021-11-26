

import pygame as pg
import time
from pygame import mixer


SCREENX = 800
SCREENY = 700
lrborder = ((SCREENX-(60*8))//2)
udborder = ((SCREENY-(60*8))//2)
turn = 1

pg.init()
mixer.init()

sound = mixer.Sound("images\\flip.mp3")

board = []  # initially output matrix is empty
for j in range(8):  # iterate to the end of rows
    row = []
    for i in range(8):  # j iterate to the end of column
        row.append(0)  # add the user element to the end of the row
    board.append(row)  # append the row to the output matrix

board[4-1][5-1] = 1
board[5-1][4-1] = 1
board[4-1][4-1] = 2
board[5-1][5-1] = 2

# for i in board:
#     for j in i:
#         print(f"{j:3}", end='')
#     print()
# for i in board:
#   print(i)

# set screen
screen = pg.display.set_mode((SCREENX, SCREENY))

# set Title and Logo
pg.display.set_caption("Reversi")
pg.display.set_icon(pg.image.load('images\go.png'))

# players
dplayerimg = pg.image.load("images\dark.png")
lplayerimg = pg.image.load("images\light.png")
emptyimg = pg.image.load("images\empty.png")


def displayer(player, x, y):
    if player == 1:
        screen.blit(dplayerimg, (x, y))
    elif player == 2:
        screen.blit(lplayerimg, (x, y))
    else:
        screen.blit(emptyimg, (x, y))


def getpos():
    x, y = pg.mouse.get_pos()
    xx = (x-lrborder)//60
    yy = (y-udborder)//60
    return xx, yy

def isonboard (x,y):
    if x >= 0 and x <= 7 and y >= 0 and y <= 7:
        return True
    else:
        return False

def validlocation(turn, posx, posy):
    """

    :param turn:
    :param posx:
    :param posy:
    :return:
    """
    oposturn = 3-turn
    fliplst = []
    if board[posx][posy] != 0:
        return fliplst
    for j in [-1,0,1]:
        for i in [-1,0,1]:
            if i==0 and j==0:
                continue
            x = posx+i
            y = posy+j
            if isonboard(x, y):
                if board[x][y] == oposturn:
                    x += i
                    y += j
                    if isonboard(x,y):
                        while board[x][y] == oposturn:
                            x += i
                            y += j
                            if not isonboard(x,y):
                                break
                        if not isonboard(x,y):
                            continue
                        if board[x][y] == turn:
                            while True:
                                x -= i
                                y -= j
                                if x == posx and y == posy:
                                    break
                                fliplst.append([x,y])
    return fliplst



def flip(fliplist, turn):
    oposturn = 3-turn
    for i,j in fliplist:
        sound.play()
        time.sleep(0.4)
        board[i][j] = turn

def possiblemove(turn):
    possible = False
    for j in range(8):
        for i in range(8):
            possible = possible or (validlocation(turn, i, j) != [])
    return possible

def changeturn():
    global turn
    turn = 3-turn
    if not possiblemove(turn):
        turn = 3-turn
        if not possiblemove(turn):
            print("game-over")
            return False
        else:
            print ("moving turn - the user didn't have a valid move")
    return True









# Game loop

running = True
while running:
    screen.fill((0, 128, 128))
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Reversi", True, (255, 255, 255))
#        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        textpos = text.get_rect(centerx=SCREENX/2, y=10)
        screen.blit(text, textpos)

    p1,p2 = 0,0
    for j in range(8):
        for i in range(8):
            displayer(board[i][j], lrborder+i*60, udborder+j*60)
            if board[i][j] == 1:
                p1 += 1
            elif board[i][j] == 2:
                p2 += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
#        print(event.type)
        if event.type == 1025:
            xx, yy = getpos()
            if isonboard(xx,yy):
                flippingcells = validlocation(turn,xx,yy)
                if flippingcells != []:
                    board[xx][yy] = turn
                    flip(flippingcells, turn)
                    changeturn()
#                   turn = 3-turn
#                   possiblemove(turn)
#                if validlocation(turn,xx,yy):
#                    marklocation(xx, yy)
#                    changeturn()
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render(str(p1), True, (255, 255, 255))
        textpos = text.get_rect(centerx=60, centery=SCREENY / 2)
        screen.blit(dplayerimg, (35, (SCREENY / 2)-90))
        screen.blit(text, textpos)
        text = font.render(str(p2), True, (255, 255, 255))
        textpos = text.get_rect(centerx=SCREENX-60, centery=SCREENY / 2)
        screen.blit(lplayerimg, ((SCREENX-85), (SCREENY / 2)-90))
        screen.blit(text, textpos)

    #    displayer(1,100,300)
#    displayer(2,700,300)

    xx, yy = getpos()
    if isonboard(xx,yy):
        if validlocation(turn,xx,yy) != []:
            displayer(turn, lrborder + xx * 60, udborder + yy * 60)

#    print(xx,yy)
    pg.display.update()
