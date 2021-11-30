

import pygame as pg
import time
from pygame import mixer
# Constants
SCREEN_X = 800
SCREEN_Y = 700
LR_BORDER = ((SCREEN_X-(60*8))//2)
UD_BORDER = ((SCREEN_Y-(60*8))//2)


class GameBoard:
    board = []  # initially output matrix is empty
    turn = 1

    def __init__(self):
        for j in range(8):  # iterate to the end of rows
            row = []
            for i in range(8):  # j iterate to the end of column
                row.append(0)  # add the user element to the end of the row
            self.board.append(row)  # append the row to the output matrix

        self.board[4-1][5-1] = 1
        self.board[5-1][4-1] = 1
        self.board[4-1][4-1] = 2
        self.board[5-1][5-1] = 2

    def isonboard(self, x, y):
        """
        Checks if x,y is on board (0-7,0-7)
        :param x: X axis
        :param y: Y axis
        :return: True if on board, False if extended the board
        """
        if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
            return True
        else:
            return False


    def validlocation(self, posx, posy):
        """

        :param posx: X axis (0-7)
        :param posy: Y axis (0-7)
        :return: empty list if is not a valid location, or list of "enemy" nodes that will be flipped if the node will be places here
        """
        oposturn = 3 - self.turn
        fliplst = []
        if self.board[posx][posy] != 0:
            return fliplst
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x = posx + i
                y = posy + j
                if self.isonboard(x, y):
                    if self.board[x][y] == oposturn:
                        x += i
                        y += j
                        if self.isonboard(x, y):
                            while self.board[x][y] == oposturn:
                                x += i
                                y += j
                                if not self.isonboard(x, y):
                                    break
                            if not self.isonboard(x, y):
                                continue
                            if self.board[x][y] == self.turn:
                                while True:
                                    x -= i
                                    y -= j
                                    if x == posx and y == posy:
                                        break
                                    fliplst.append([x, y])
        return fliplst


    def possiblemove(self):
        """
        Checks if the current player has an available location
        :return: True if there is a possible location, False if there is no available location
        """
        possible = False
        for j in range(8):
            for i in range(8):
                possible = possible or (self.validlocation(i, j) != [])
        return possible


    def changeturn(self):
        """
        Change the current playing player, and checks if he has possible location,
            If not - the current player will be changed - If both will not have available location - the game will end.
        :return: False if the game is over , True otherwise.
        """
        self.turn = 3-self.turn
        if not self.possiblemove():
            self.turn = 3-self.turn
            if not self.possiblemove():
                return False #  "game-over"
        return True  #   "moving turn - the user didn't have a valid move"

#game initialization
cont = True
pg.init()
mixer.init()
sound = mixer.Sound("images\\flip.mp3")
game = GameBoard()


# set screen
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y))


# set Title and Logo
pg.display.set_caption("Reversi")
pg.display.set_icon(pg.image.load('images\\go.png'))

# players images
dplayerimg = pg.image.load("images\\dark.png")
lplayerimg = pg.image.load("images\\light.png")
emptyimg = pg.image.load("images\\empty.png")


def displayer(player, x, y):
    """
    Draws the board on the screen according to the player
    :param player: The player (color) that needs to be placed on the screen (including empty one - 0).
    :param x: X axis of the placement
    :param y: Y axis of the placement
    :return:
    """
    if player == 1:
        screen.blit(dplayerimg, (x, y))
    elif player == 2:
        screen.blit(lplayerimg, (x, y))
    else:
        screen.blit(emptyimg, (x, y))


def getpos():
    """
    turns the X,Y axis of the mouse into places in the 8X8 board
    :return: XX and YY - places on the boards (0-7,0-7)
    """
    x, y = pg.mouse.get_pos()
    xx = (x-LR_BORDER)//60
    yy = (y-UD_BORDER)//60
    return xx, yy






def flip(fliplist, turn):
    """
    The function will flip the "enemy" nodes into player nodes (was calculated in the validlocation function
    :param fliplist: a list of nodes (x,y) that needs to be flipped
    :param turn: the current player (color)
    :return:
    """
    oposturn = 3-turn
    for i,j in fliplist:
        sound.play()
        time.sleep(0.4)
        game.board[i][j] = turn



def write(txt, x, y):
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render(txt, True, (255, 255, 255))
        textpos = text.get_rect(centerx=x, centery=y)
        screen.blit(text, textpos)
        pg.display.update()


def gameover():
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("WON !!!", True, (255, 255, 255))
        textpos = text.get_rect(centerx=SCREEN_X /2, centery=SCREEN_Y - 50)
        if p2>p1:
            screen.blit(lplayerimg, (SCREEN_X /2 - 180, SCREEN_Y-80))
            screen.blit(text, textpos)
        elif p1>p2:
            screen.blit(dplayerimg, ((SCREEN_X/2 - 180), (SCREEN_Y - 80)))
            screen.blit(text, textpos)
        else:
            text = font.render(" BOTH WON !!!", True, (255, 255, 255))
            screen.blit(text, textpos)
        pg.display.update()
        time.sleep(15)








# Game loop

running = True
while running:
    screen.fill((0, 128, 128))
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Reversi", True, (255, 255, 255))
#        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        textpos = text.get_rect(centerx=SCREEN_X/2, y=10)
        screen.blit(text, textpos)

    p1,p2 = 0,0
    for j in range(8):
        for i in range(8):
            displayer(game.board[i][j], LR_BORDER+i*60, UD_BORDER+j*60)
            if game.board[i][j] == 1:
                p1 += 1
            elif game.board[i][j] == 2:
                p2 += 1
    if not cont:
        gameover()
        running = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
#        print(event.type)
        if event.type == 1025:
            xx, yy = getpos()
            if game.isonboard(xx,yy):
                flippingcells = game.validlocation(xx,yy)
                if flippingcells != []:
                    game.board[xx][yy] = game.turn
                    flip(flippingcells, game.turn)
                    cont = game.changeturn()

#                   game.turn = 3-game.turn
#                   possiblemove(game.turn)
#                if validlocation(game.turn,xx,yy):
#                    marklocation(xx, yy)
#                    changeturn()
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render(str(p1), True, (255, 255, 255))
        textpos = text.get_rect(centerx=60, centery=SCREEN_Y / 2)
        screen.blit(dplayerimg, (35, (SCREEN_Y / 2)-90))
        screen.blit(text, textpos)
        text = font.render(str(p2), True, (255, 255, 255))
        textpos = text.get_rect(centerx=SCREEN_X-60, centery=SCREEN_Y / 2)
        screen.blit(lplayerimg, ((SCREEN_X-85), (SCREEN_Y / 2)-90))
        screen.blit(text, textpos)

    #    displayer(1,100,300)
#    displayer(2,700,300)


    xx, yy = getpos()
    if game.isonboard(xx,yy):
        if game.validlocation(xx,yy) != []:
            displayer(game.turn, LR_BORDER + xx * 60, UD_BORDER + yy * 60)

#    print(xx,yy)
    pg.display.update()
