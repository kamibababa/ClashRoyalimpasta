import pygame, UI, sys, time, random, grid, card, Hero,Bullet,startMode, KeyboardCardSelector, joystick,endMode
from PIL import Image, ImageDraw
from pygame.locals import *
from UI import *
from pygame.locals import *



pygame.init()

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONUP,MOUSEBUTTONDOWN])
joystick.main()

flags = FULLSCREEN | DOUBLEBUF

pygame.display.set_caption('Clash Impasta')

Display = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT),flags)

Display.set_alpha(None)

#GameTime = remainingTime --> 150000 ---> 2.5min
initTime = 150000
remainingTime = initTime
extraTime=60000
isGameEnded = False
inExtraTime = False

Grid = grid.Grid()
Selector = [selector.CardSelector(0), selector.CardSelector(1)]
CardPointer = KeyboardCardSelector.CardPointer(Selector[0], Grid)

currentHeros = [[], []]
currenTowers=[[],[]]
currentBullets = []
error_sound = pygame.mixer.Sound('Sounds/badswap.wav')

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def addHero(x,y,Name,Side,is_tower):
    new_hero = Hero.Hero(x,y,Name,Side,is_tower)
    currentHeros[Side].append(new_hero)
    Grid.mat[y][x] = new_hero
    if is_tower == True:
        currenTowers[Side].append(new_hero)

background_surface = UI.buildBackground()

def updateUI():
    Display.blit(background_surface, (0, 0))
    UI.blitLeftSelector(Selector[0], Display, pygame.time.get_ticks())
    UI.blitRightSelector(Selector[1], Display, pygame.time.get_ticks())
    UI.blitGrid(Grid, Display)
    UI.blitKeyboardSelector(CardPointer, Display)
    #new
    UI.blitBullets(currentBullets,Display)
    UI.blitDecorations(Display)
  #new new
    UI.blitTimer(Display,remainingTime,inExtraTime)


def init():
    names = ['Soldier', 'Knight', 'Viking', 'Zombie', 'Ninja', 'Soldier76', 'Big_Hero']
    for i in range(7):
        Selector[0].addCard(card.Card(side_ = 0, name_ = names[i]))
        Selector[1].addCard(card.Card(side_ = 1, name_ = names[i]))
    addHero(0,  2, "Small_Tower", 0, True)
    addHero(0,  5, "Big_Tower",   0, True)
    addHero(0, 10, "Small_Tower", 0, True)

    addHero(19,  2, "Small_Tower", 1, True)
    addHero(19,  5, "Big_Tower",   1, True)
    addHero(19, 10, "Small_Tower", 1, True)

def errorSound():
    error_sound.play()

init()

def checkForEnd():

    global inExtraTime,remainingTime

    if currenTowers[0][1].is_alive == False:
            endMode.main(Display,True)

    if currenTowers[1][1].is_alive == False:
            endMode.main(Display,False)

    if inExtraTime == False and remainingTime < 50:
        cnt0=0
        cnt1=0
        if currenTowers[0][0].is_alive == False:
            cnt0+=1
        if currenTowers[0][2].is_alive == False:
            cnt0+=1
        if currenTowers[1][0].is_alive == False:
            cnt1+=1
        if currenTowers[1][2].is_alive == False:
            cnt1+=1
        if cnt1 != cnt0:
            endMode.main(Display,cnt0 > cnt1)
        inExtraTime = True

    elif inExtraTime == True and remainingTime < 50:
        right = currenTowers[1][0].health + currenTowers[1][2].health + currenTowers[1][1].health
        left = currenTowers[0][0].health + currenTowers[0][2].health + currenTowers[0][1].health
        endMode.main(Display,right > left)


mouseX, mouseY = 0, 0
dX, dY = 0, 0

mouseClicked = False

selected_card = None
selected_card2 = None

cnt = 0

clock = pygame.time.Clock()
clock.tick(60)

flagai = 0

isGameStarted = False
if isGameStarted == False:
    flagai = startMode.main(Display)
print('flagai', flagai)

# 0 ------> player vs player
# 1 ------> player vs computer
delayTime = pygame.time.get_ticks()

last_card_added_time = 0

def aiDecide():
    global last_card_added_time
    selected_dmg = 100000
    ind = 0
    if (pygame.time.get_ticks() - last_card_added_time < 1000):
        return
    for i in range (len(Selector[0].card_list)):
        selected_card = Selector[0].card_list[i]
        if (Data.Heros_Dic[selected_card.name]["DAMAGE_RATE"] < selected_dmg and 
            pygame.time.get_ticks() - selected_card.av_time > Data.Heros_Dic[selected_card.name]["LOADTIME"]):
            selected_dmg = Data.Heros_Dic[selected_card.name]["DAMAGE_RATE"]
            ind = i
    flag3 = False
    for i in range(Grid.height - 3, 3, -1):
        if (flag3):
            break
        for j in range(3, Grid.width // 2):
            if (Grid.mat[i][j] == 0):
                addHero(j, i, Selector[0].card_list[ind].name, Selector[0].card_list[ind].side, False)
                Selector[0].card_list[ind].av_time = pygame.time.get_ticks()
                last_card_added_time = pygame.time.get_ticks()
                flag3 = True
                break
while True:
    remainingTime = initTime - ( pygame.time.get_ticks() - delayTime)
    if inExtraTime == True :
        remainingTime += extraTime
    cnt += 1
    Display.fill(LIGHT_YELLOW)
    updateUI()
    checkForEnd()
    checkForQuit()
    mouseX, mouseY = pygame.mouse.get_pos()
    Hero.herosProcess(Grid,currentHeros, currentBullets, cnt)
    Bullet.bulletsProcess(Grid,currentBullets)
    grid.updateGrid(Grid, currentHeros)
    if (flagai):
        aiDecide()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouseClicked = True
            selected_card = selector.getSelectorCard(mouseX, mouseY, Selector[0])
            if selected_card == None:
                selected_card = selector.getSelectorCard(mouseX, mouseY, Selector[1])
            if (selected_card != None):
                dX, dY = mouseX - selected_card.box[0], mouseY - selected_card.box[1]
                if (pygame.time.get_ticks() - selected_card.av_time > Data.Heros_Dic[selected_card.name]["LOADTIME"]):
                    selected_card.av_time = pygame.time.get_ticks()
                else:
                    selected_card = None

            #print(selected_card)
        elif event.type == MOUSEBUTTONUP:
            pos = Grid.getCellByPixel(mouseX, mouseY)
            if (pos[1] >= Grid.height or pos[0] >= Grid.width or pos[1] < 0 or pos[0] < 0):
                errorSound()
                mouseClicked = False
                selected_card = None
            if (selected_card != None):
                if (Grid.get(pos[1], pos[0]) == 0 and ((selected_card.side == 0 and pos[0] < Grid.width // 2) or (selected_card.side == 1 and pos[0] >= Grid.width // 2))):
                    addHero(pos[0], pos[1], selected_card.name, selected_card.side, False)
                else:
                    errorSound()
            mouseClicked = False
            selected_card = None
        elif event.type == KEYDOWN:
          if (event.key == K_DOWN):
            CardPointer.down()
          elif (event.key == K_UP):
            CardPointer.up()
          elif (event.key == K_RIGHT):
            CardPointer.right()
          elif (event.key == K_LEFT):
            CardPointer.left()
          elif (event.key == K_RETURN):
            if selected_card2 != None:
                if CardPointer.on_grid and Grid.mat[CardPointer.r][CardPointer.c] == 0 and CardPointer.c < Grid.width // 2:
                    addHero(CardPointer.c, CardPointer.r + 1, selected_card2.name, selected_card2.side, False)
                    selected_card2 = None
                else:
                    errorSound()
            else:
                if (CardPointer.on_grid == False):
                    selected_card2 = Selector[0].card_list[CardPointer.r]
                    if (pygame.time.get_ticks() - selected_card2.av_time > Data.Heros_Dic[selected_card2.name]["LOADTIME"]):
                        selected_card2.av_time = pygame.time.get_ticks()
                    else:
                        selected_card2 = None
        if (joystick.flag):
            pressed_key = joystick.getPressedKey()
            if (pressed_key == 'up'):
                CardPointer.up()
            elif (pressed_key == 'down'):
                CardPointer.down()
            elif (pressed_key == 'left'):
                CardPointer.left()
            elif (pressed_key == 'right'):
                CardPointer.right()
            elif (pressed_key == 'A'):
                if selected_card2 != None:
                    if CardPointer.on_grid and Grid.mat[CardPointer.r][CardPointer.c] == 0 and CardPointer.c < Grid.width // 2:
                        addHero(CardPointer.c, CardPointer.r + 1, selected_card2.name, selected_card2.side, False)
                        selected_card2 = None
                    else:
                        errorSound()
                else:
                    if (CardPointer.on_grid == False):
                        selected_card2 = Selector[0].card_list[CardPointer.r]
                        if (pygame.time.get_ticks() - selected_card2.av_time > Data.Heros_Dic[selected_card2.name]["LOADTIME"]):
                            selected_card2.av_time = pygame.time.get_ticks()
                        else:
                            selected_card2 = None
            
    if mouseClicked == True and selected_card != None:
        Display.blit(selected_card.image, (mouseX - dX, mouseY - dY))
    pygame.display.update()
