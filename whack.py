import pygame, random, sys, math
from pygame.locals import *

pygame.font.init()
class writerMine:
    def __init__(self, fonter = 't'):
        self.fonts = []
        for i in range(0, 100):
            self.fonts.append(i)
            #print(i)
        self.fontuse = fonter

    def addFont(self, size):
        self.fonts[size - 1] = pygame.font.SysFont(self.fontuse, size)

    def write(self, size, text):
        #print(str(size) + ', ' + text)
        text = str(text)
        if self.fonts[size - 1] == size - 1: self.addFont(size)
        disper = self.fonts[size - 1].render(text, True, (255, 255 , 255))
        return disper

FPS = 60
RES = (600, 400)
GAMERES = (RES[0] - 200, RES[1] - 100)
dispsurf = pygame.display.set_mode(RES)
gamesurf = pygame.Surface(GAMERES)
gamesurf.fill((0, 200, 255))
pygame.draw.rect(gamesurf, (0, 255, 0), (0, GAMERES[1] - (GAMERES[1] - 66), GAMERES[0], GAMERES[1] - 66))
bgsurf = gamesurf.copy()
bsurf = dispsurf.copy()
FPSCLOCK = pygame.time.Clock()
sprites = pygame.sprite.Group()
score = 0
WRITER = writerMine()
paused = False

# class target(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.frame = 0
#         self.images = []
#         for i in range(0, 40):
#             self.images.append(pygame.Surface((10, 10)))
#             self.images[i].fill((12.5 * abs(20 - i), 100, 100))
#         self.image = self.images[self.frame]
#         self.rect = self.image.get_rect()
#         self.rect[0], self.rect[1] = x, y
#         self.time = pygame.time.get_ticks()
#
#     def update(self):
#         self.frame += 1
#         self.frame = self.frame % len(self.images)
#         self.image = self.images[self.frame]


def recolor(a, b):
    #print(a.unmap_rgb(pygame.PixelArray(a)[32][32]))
    working = pygame.PixelArray(a)
    for x in range(0, len(working)):
        for y in range(0, len(working[x])):
            colornow = tuple(a.unmap_rgb(working[x][y]))
            #colornow = (a.unmap_rgb(working[x][y])[0], a.unmap_rgb(working[x][y])[1], a.unmap_rgb(working[x][y])[2], a.unmap_rgb(working[x][y])[3])
            if(colornow in b):
                working[x][y] = b[colornow]

SHIRTCOLORS = [
    (88, 25, 25, 255),
    (132, 55, 6, 255),
    (255, 180, 133, 255),
    (42, 50, 107, 255),
    (28, 31, 47, 255),
    (38, 58, 21, 255),
    (240, 255, 230, 255),
    (140, 135, 40, 255),
    (15, 80, 50, 255),
    (70, 255, 170, 255)
]

PANTCOLORS = [
    (88, 25, 25, 255),
    (132, 55, 6, 255),
    (255, 180, 133, 255),
    (42, 50, 107, 255),
    (28, 31, 47, 255),
    (38, 58, 21, 255),
    (240, 255, 230, 255),
    (140, 135, 40, 255),
    (15, 80, 50, 255),
    (70, 255, 170, 255)
]

SKINCOLORS = [
    (255, 220, 110, 255),
    (250, 220, 120, 255),
    (255, 230, 170, 255),
    (215, 140, 80, 255),
    (250, 180, 120, 255),
    (115, 85, 55, 255),
    (180, 115, 60, 255),
    (170, 90, 25, 255),
    (100, 70, 40, 255),
    (90, 50, 40, 255)
]

class target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame = 0
        self.cont = 0
        self.conta = 0
        self.images = []
        shirtcolor = SHIRTCOLORS[random.randint(0, len(SHIRTCOLORS) - 1)]
        pantcolor = PANTCOLORS[random.randint(0, len(SHIRTCOLORS) - 1)]
        skincolor = SKINCOLORS[random.randint(0, len(SHIRTCOLORS) - 1)]
        for i in range(1, 4):
            self.images.append(pygame.transform.scale(pygame.image.load('man' + str(i) + '.png'), (64, 64)))
            recolor(self.images[i - 1], {
                (64, 35, 8, 255): shirtcolor,
                (68, 55, 7, 255): pantcolor,
                (214, 142, 77, 255): skincolor
            })
            #print('man' + str(i) + '.png', self.images[i - 1])
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = x, y
        #self.time = pygame.time.get_ticks()

    def update(self):
        self.cont += .1
        self.cont += score / 250
        #print(self.cont)
        #if(int(self.cont) > 0): print(self.rect, self.cont, self.conta)
        self.rect[0] -= int(self.cont) * 5
        self.conta += int(self.cont)
        self.frame += int(self.cont)
        self.cont -= int(self.cont)
        self.frame = self.frame % len(self.images)
        self.image = self.images[self.frame]

class cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('cloud.png'), (50, 35))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = 100, 100
        self.cycle = 0

    def update(self):
        self.rect[1] -= (math.sin(self.cycle) * 50)
        self.cycle += .1
        #print(self.cycle, math.sin(self.cycle), self.rect[1])
        self.rect[1] += (math.sin(self.cycle) * 50)
        #recolor(self.image)


class aimer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('target.png')
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = 100, 100

class bolt(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('bolt.png')
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = pos[0] + 12, pos[1] - 50
        self.count = 0

    def update(self):
        if(self.count == 11):
            self.kill()
        self.rect[1] += 5
        self.rect[0] += random.randint(-2, 2)
        self.count += 1

class zap(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.bg = pygame.Surface((32, 32))
        self.image = self.bg.convert_alpha(self.bg)
        pygame.draw.circle(self.image, (255, 255, 255), (16, 16), (1))
        self.image.fill((255, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = pos[0] - 16, pos[1] - 16
        self.age = 1

    def update(self):
        self.image = self.bg.convert_alpha(self.bg)
        self.image.fill((255, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (16, 16), int(math.sin(self.age / 25 * math.pi) * 10))
        self.age += 1
        if self.age >= 25:
            self.kill()
        if(self.age % 4 == 0):
            for i in range(1, 20):
                arange = random.randint(0, 16)
                angle = random.randint(0, 360)
                x = 16 + arange * math.cos(angle / 180 * math.pi)
                y = 16 + arange * math.sin(angle / 180 * math.pi)
                #print(x, y)
                #if(not (1 < x < 31) or not (1 < y < 31)):
                    #print(arange, angle, x, y)
                pygame.draw.rect(self.image, (255, 255, random.randint(0, 50)), (x, y, 6, 6))

def time_format(ticks):
    ticks = int(ticks / 1000)
    return str(int(ticks / 60)) + ':' + str(ticks % 60) if (ticks % 60) > 9 else str(int(ticks / 60)) + ':0' + str(ticks % 60)

def bound(minVal, val, maxVal):
    return(max(minVal, min(val, maxVal)))

pygame.mouse.set_visible(False)
test = target(300, 100)
#print(test.rect)
zeus = cloud()
aim = aimer()
gods = pygame.sprite.Group(zeus, aim)
bolts = pygame.sprite.Group()
temp = pygame.sprite.Group()
zaps = pygame.sprite.Group()
sprites.add(test)
print(pygame.USEREVENT, pygame.NUMEVENTS)
pygame.time.set_timer(25, 500)
tries = 0
while(True):
    #if(not paused): pygame.mouse.set_pos((bound(100, pygame.mouse.get_pos()[0], 100 + GAMERES[0])), bound(50, pygame.mouse.get_pos()[1], 50 + GAMERES[1]))
    zeus.rect[0], zeus.rect[1] = bound(0 - zeus.rect[2] / 2, pygame.mouse.get_pos()[0] - 125, GAMERES[0] - zeus.rect[2] / 2), bound(0, pygame.mouse.get_pos()[1] - 117.5, GAMERES[1] - zeus.rect[3] / 2 - 50)
    aim.rect[0], aim.rect[1] = bound(0 - aim.rect[2] / 2, pygame.mouse.get_pos()[0] - (16 + 100), GAMERES[0] - aim.rect[2] / 2), bound(50, pygame.mouse.get_pos()[1] - (16 + 50), GAMERES[1] - aim.rect[3] / 2)
    #print(zeus.rect)
    sprites.update()
    gods.update()
    bolts.update()
    zaps.update()
    zaps.clear(gamesurf, bgsurf)
    gods.clear(gamesurf, bgsurf)
    bolts.clear(gamesurf, bgsurf)
    dispsurf.blit(bsurf, (0, 0))
    for bolto in bolts:
        if(bolto.count == 10):
            # bang = pygame.sprite.Sprite()
            # bang.rect = bolto.rect
            # bang.rect[0], bang.rect[1] = bolto.rect[0] - 5, bolto.rect[1] + (bolto.rect[3] / 2 - 15)
            # bang.rect[2], bang.rect[3] = 20, 20
            # bang.image = pygame.Surface((20, 20))
            zaps.add(zap((bolto.rect[0] + 8, bolto.rect[1] + (bolto.rect[3] / 2))))
            # print(bang.rect)
            #temp.add(bang)
            #FPSCLOCK.tick(1)
    for zapper in zaps:
        for sprit in pygame.sprite.spritecollide(zapper, sprites, False):
            score += 1
            sprites.remove(sprit)
    for sprit in sprites:
        # if sprit.time <= pygame.time.get_ticks() - (50 * max(100 - score, 10)):
        #     sprites.remove(sprit)
        if sprit.rect[0] < 0 - sprit.rect[3]:
            score -= 1
            sprites.remove(sprit)
    sprites.clear(gamesurf, bgsurf)
    sprites.draw(gamesurf)
    temp.draw(gamesurf)
    gods.draw(gamesurf)
    bolts.draw(gamesurf)
    zaps.draw(gamesurf)
    #print(len(sprites))
    #sprites.empty()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == 25:
            pygame.time.set_timer(25, max(50, 500 - (score * 2)))
            newsprit = target(random.randint(GAMERES[0] * .9, GAMERES[0] - 10), random.randint(66, GAMERES[1] - 30))
            if(tries > 50):
                tries = 0
                break
            if len(pygame.sprite.spritecollide(newsprit, sprites, False)) > 0:
                tries += 1
                pygame.event.post(pygame.event.Event(25))
            else:
                sprites.add(newsprit)
                tries = 0
        if event.type == MOUSEBUTTONDOWN:
            # mousespot = pygame.sprite.Sprite()
            # #mousespot.image = pygame.Surface((0, 0))
            # mousespot.rect = Rect(aim.rect[0], aim.rect[1], 60, 60)
            # #pygame.sprite.GroupSingle(mousespot).draw(gamesurf)
            # for sprit in pygame.sprite.spritecollide(mousespot, sprites, False):
            #     score += 1
            #     sprites.remove(sprit)
            bolts.add(bolt((aim.rect[0], aim.rect[1])))
        if event.type == KEYDOWN:
            paused = not paused

    # while(paused):
    #     for event in pygame.event.get():
    #         if event.type == KEYDOWN:
    #             paused = not paused
    dispsurf.blit(gamesurf, (100, 50))
    dispsurf.blit(WRITER.write(30, score), (10, 180))
    dispsurf.blit(WRITER.write(30, time_format(pygame.time.get_ticks())), (275, 20))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
