import os
import random
import sys
import urllib.request
import zipfile
import ctypes
import pygame


class Tank(pygame.sprite.Sprite):
    T = pygame.sprite.Group()

    def __init__(self):
        self.image = pygame.image.load('tank_P_0.png')
        self.image1 = self.image.subsurface(0, 0, 48, 48)
        self.rect = self.image1.get_rect()
        self.rect.topleft = (250, 700)

    def move(self, way):
        self.status = True
        if pygame.sprite.spritecollide(self, Brick.B_group, False):
            self.status = False
        elif pygame.sprite.spritecollide(self, River.R_group, False):
            self.status = False
        elif pygame.sprite.spritecollide(self, Ice.I_group, True):
            self.status = False
        elif pygame.sprite.spritecollide(self, Iron.O_group, False):
            self.status = False
        elif self.rect.left < 0 or self.rect.right > 800 or self.rect.top < 0 or self.rect.bottom > 780:
            self.status = False
        else:
            self.status = True

        if way == 'up':
            if self.status == False:
                self.rect = self.poss
                channel2 = music2.play()
            else:
                self.poss = self.rect
                self.image1 = self.image.subsurface(0, 0, 48, 48)
                self.rect = self.rect.move((0, -3))

        if way == 'down':
            if self.status == False:
                self.rect = self.poss
                channel2 = music2.play()
            else:
                self.poss = self.rect
                self.image1 = self.image.subsurface(0, 48, 48, 48)
                self.rect = self.rect.move((0, 3))

        if way == 'left':
            if self.status == False:
                self.rect = self.poss
                channel2 = music2.play()
            else:
                self.poss = self.rect
                self.image1 = self.image.subsurface(0, 96, 48, 48)
                self.rect = self.rect.move((-3, 0))

        if way == 'right':
            if self.status == False:
                self.rect = self.poss
                channel2 = music2.play()
            else:
                self.poss = self.rect
                self.image1 = self.image.subsurface(0, 144, 48, 48)
                self.rect = self.rect.move((3, 0))


class Brick(pygame.sprite.Sprite):
    B_group = pygame.sprite.Group()

    def __init__(self, pos, path, ):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect(topleft=pos)
        self.B_group.add(self)


class Tree(pygame.sprite.Sprite):
    T_group = pygame.sprite.Group()

    def __init__(self, pos, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect(topleft=pos)
        self.T_group.add(self)


class River(pygame.sprite.Sprite):
    R_group = pygame.sprite.Group()
    count = 0
    a = True

    def __init__(self, pos, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load('river2.png')
        self.image2 = pygame.image.load('river.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.R_group.add(self)

    @classmethod
    def show(cla,screen):
        for river in River.R_group:
            if River.count % 8 == 0:
                River.a = not River.a
            if River.a:
                screen.blit(river.image, river.rect)
            else:
                screen.blit(river.image2, river.rect)

            River.count += 1


class Ice(pygame.sprite.Sprite):
    I_group = pygame.sprite.Group()

    def __init__(self, pos, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect(topleft=pos)
        self.I_group.add(self)


class Iron(pygame.sprite.Sprite):
    O_group = pygame.sprite.Group()

    def __init__(self, pos, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect(topleft=pos)
        self.O_group.add(self)


class Bullet(pygame.sprite.Sprite):
    bullet_group = pygame.sprite.Group()
    time = 0
    count = 1

    def __init__(self, pos, way):
        super().__init__()

        if way == 'up':
            self.path = 'up.png'
            self.rect = pygame.Rect(pos.left + 17, pos.top, 8, 8)
        elif way == 'down':
            self.path = 'down.png'
            self.rect = pygame.Rect(pos.left + 17, pos.top + 50, 8, 8)
        elif way == 'left':
            self.path = 'left.png'
            self.rect = pygame.Rect(pos.left - 15, pos.top + 20, 8, 8)
        elif way == 'right':
            self.path = 'right.png'
            self.rect = pygame.Rect(pos.left + 40, pos.top + 18, 8, 8)

        self.image = pygame.image.load(self.path)
        self.bullet_group.add(self)
        self.way = way

    @classmethod
    def show(cls, screen):
        for bullet in Bullet.bullet_group:
            screen.blit(bullet.image, bullet.rect)

    @classmethod
    def move(cls):
        for bullet in Bullet.bullet_group:
            if bullet.rect.left < 0 or bullet.rect.right > 830 or bullet.rect.top < 0 or bullet.rect.bottom > 780 or pygame.sprite.spritecollide(
                    bullet, Brick.B_group, True) or pygame.sprite.spritecollide(bullet, Iron.O_group, False):
                Bullet.bullet_group.remove(bullet)
                channel3 = music2.play()
                del bullet
                Bullet.count += 1
                continue
            if bullet.way == 'up':
                bullet.rect = bullet.rect.move(0, -5)
            elif bullet.way == 'down':
                bullet.rect = bullet.rect.move(0, 5)
            elif bullet.way == 'left':
                bullet.rect = bullet.rect.move(-5, 0)
            elif bullet.way == 'right':
                bullet.rect = bullet.rect.move(5, 0)


class Enemy(pygame.sprite.Sprite):
    enemy_group = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        self.dir = random.choice(['up', 'down', 'right', 'left'])
        if self.dir == 'up':
            self.image = pygame.image.load('enemy.png').subsurface((0, 0, 48, 48))
        elif self.dir == "down":
            self.image = pygame.image.load('enemy.png').subsurface((0, 48, 48, 48))
        elif self.dir == "left":
            self.image = pygame.image.load('enemy.png').subsurface((0, 96, 48, 48))
        elif self.dir == "right":
            self.image = pygame.image.load('enemy.png').subsurface((0, 144, 48, 48))
        self.rect = pygame.Rect(pos, (48, 48))
        self.enemy_group.add(self)

    @classmethod
    def show(self, screen):
        for enemy in Enemy.enemy_group:
            screen.blit(enemy.image, enemy.rect)

    @classmethod
    def move(cls):
        status = True
        for enemy in Enemy.enemy_group:

            '''if enemy.rect.left < 0 or enemy.rect.right > 810 or enemy.rect.top < 0 or enemy.rect.bottom > 780 or pygame.sprite.spritecollide(
                    enemy, Ice.I_group, False) or pygame.sprite.spritecollide(enemy, River.R_group, False):'''
            if enemy.rect.left < 0:
                enemy.dir = 'right'

            if enemy.rect.right > 810:
                enemy.dir = 'left'

            if enemy.rect.top < 0:
                enemy.dir = 'down'
            if pygame.sprite.spritecollide(enemy, Ice.I_group, False) or pygame.sprite.spritecollide(enemy,
                                                                                                     River.R_group,
                                                                                                     False):
                enemy.dir = 'up'

            if enemy.dir == 'up':
                enemy.rect = enemy.rect.move(0, -1)
                enemy.image = pygame.image.load('enemy.png').subsurface((0, 0, 48, 48))
            elif enemy.dir == 'down':
                enemy.rect = enemy.rect.move(0, 1)
                enemy.image = pygame.image.load('enemy.png').subsurface((0, 48, 48, 48))
            elif enemy.dir == 'left':
                enemy.rect = enemy.rect.move(-1, 0)
                enemy.image = pygame.image.load('enemy.png').subsurface((0, 96, 48, 48))
            elif enemy.dir == 'right':
                enemy.rect = enemy.rect.move(1, 0)
                enemy.image = pygame.image.load('enemy.png').subsurface((0, 144, 48, 48))

            if pygame.sprite.spritecollide(enemy, Bullet.bullet_group, True):
                Enemy.enemy_group.remove(enemy)
                channel3 = music2.play()
                del enemy
                Bullet.count += 1
if os.path.exists('tank.zip'):
    pass
else:
    url1 = 'https://2222-1317600699.cos.ap-nanjing.myqcloud.com/tank.zip'
    urllib.request.urlretrieve(url1, 'tank.zip')
    with zipfile.ZipFile('tank.zip', 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
way = 'up'
pygame.init()
tank1 = Tank()
music1 = pygame.mixer.Sound("start.wav")
music2 = pygame.mixer.Sound("blast.wav")
music3 = pygame.mixer.Sound("hit.wav")
music1.set_volume(0.2)
music2.set_volume(0.2)
channel1 = music1.play(loops=-1)
imagec = pygame.image.load('home.png')
imageb = pygame.image.load('background.jpg')
screen = pygame.display.set_mode((800, 780))
pygame.display.set_caption('坦克大战    按方向键移动，按空格发射炮弹')
screen.blit(imageb, (0, 0))
clock = pygame.time.Clock()
font = pygame.font.Font('1.TTF', 40)
with open('easy.txt', "r") as f:
    num_rows = 0
    for line in f.readlines():
        line = line.strip("\n")
        for num_col, element in enumerate(line.split(" ")):
            position = 24 * num_col, 24 * num_rows
            if element == "B":
                Brick(position, "brick.png")
            elif element == "I":
                Ice(position, "ice.png")
            elif element == "O":
                Iron(position, "iron.png")
            elif element == "R":
                River(position, "river.png")
            elif element == "T":
                Tree(position, "tree.png")
        num_rows += 1
for _ in range(6):
    number1 = random.randrange(1, 800, 100)
    number2 = random.randrange(1, 200, 50)
    Enemy((number1, number2))
while True:
    Bullet.move()

    screen.blit(imageb, (0, 0))
    screen.blit(imagec, (360, 740))
    screen.blit(tank1.image1, tank1.rect)
    Enemy.show(screen)
    Ice.I_group.draw(screen)
    Iron.O_group.draw(screen)
    Brick.B_group.draw(screen)
    River.show(screen)
    Tree.T_group.draw(screen)
    Bullet.show(screen)
    text_surface = font.render(f"剩余敌方坦克{len(Enemy.enemy_group)}", True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (650, 740)
    screen.blit(text_surface, text_rect)
    Enemy.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        tank1.move('up', )
        way = 'up'
    elif keys[pygame.K_DOWN]:
        tank1.move('down', )
        way = 'down'
    elif keys[pygame.K_LEFT]:
        tank1.move('left', )
        way = 'left'
    elif keys[pygame.K_RIGHT]:
        way = 'right'
        tank1.move('right', )
    if keys[pygame.K_SPACE] and Bullet.count >= 1:
        channel4 = music3.play()
        Bullet(tank1.rect, way)
        Bullet.count -= 1
    if len(Enemy.enemy_group) == 0:
        image_end = pygame.image.load('win.jpg')
        screen.blit(image_end, (0, 0))
        pygame.mixer.stop()

    clock.tick(60)
    pygame.display.update()
