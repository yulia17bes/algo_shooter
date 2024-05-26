#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y  = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
    
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
h = 3
goal = 10
max_lost = 3

win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_w, win_h))

font.init()
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', 1, (255, 255, 255))
lose = font1.render('YOU LOSE!', 1, (180, 0, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

player = Player('rocket.png', 310, win_h - 115, 85, 100, 4)
speed_ufo = randint(1, 3)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), randint(-200, 0), 80, 50, randint(1, 3)) 
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy('asteroid.png', randint(80, win_w - 80), randint(-200, 0), 80, 50, randint(1, 3)) 
    asteroids.add(asteroid) 
bullets = sprite.Group()

clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        window.blit(background, (0, 0))
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_h = font2.render('Количество жизней: ' + str(h), 1, (255, 255, 255))
        window.blit(text_h, (10, 80))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(player, asteroids, True):
            h -= 1
            asteroid = Enemy('asteroid.png', randint(80, win_w - 80), randint(-200, 0), 80, 50, randint(1, 3)) 
            asteroids.add(asteroid) 

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(background, (0, 0))
            monsters.draw(window)
            asteroids.draw(window)
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(background, (0, 0))
            player.reset()
            window.blit(win, (200, 200))

        if h <= 0:
            finish = True
            window.blit(background, (0, 0))
            monsters.draw(window)
            asteroids.draw(window)
            window.blit(lose, (200, 200))

    display.update()
    clock.tick(FPS)


'''
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y  = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
    
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
goal = 10
max_lost = 3

win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_w, win_h))

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', 1, (255, 255, 255))
lose = font1.render('YOU LOSE!', 1, (180, 0, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

player = Player('rocket.png', 310, win_h - 115, 85, 100, 4)
speed_ufo = randint(1, 3)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), randint(-200, 0), 80, 50, randint(1, 3)) 
    monsters.add(monster)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        window.blit(background, (0, 0))
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)

'''