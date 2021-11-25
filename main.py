

import pygame as pg

SCREENX = 800
SCREENY = 700
lrborder = ((SCREENX-(60*8))//2)
udborder = ((SCREENY-(60*8))//2)

pg.init()

board = []  # initially output matrix is empty
for i in range(8):  # iterate to the end of rows
    row = []
    for j in range(8):  # j iterate to the end of column
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
pg.display.set_icon(pg.image.load('go.png'))

# players
dplayerimg = pg.image.load("dark.png")
lplayerimg = pg.image.load("light.png")
emptyimg = pg.image.load("empty.png")


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

def validlocation():
    valid = False
    possibilities = []
    for i in range (-1,2):
        for j in range (-1,2):
            if xx+i<8 and xx+i>-1 and yy+j<8 and yy-j>-1 and (i !=0 or j!=0):
                


# Game loop
turn = 1
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
    for i in range(8):
        for j in range(8):
            displayer(board[i][j], lrborder+j*60, udborder+i*60)
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
            if xx >= 0 and xx <= 7 and yy >= 0 and yy <= 7:
#                board[yy][xx] = 2
                if validlocation(turn,xx,yy):
                    marklocation(xx, yy)
                    changeturn()
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
    if xx >= 0 and xx <= 7 and yy >= 0 and yy <= 7:
        displayer(2, lrborder + xx * 60, udborder + yy * 60)

#    print(xx,yy)
    pg.display.update()
