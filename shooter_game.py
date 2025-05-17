from pygame import *
from random import randint 
import pygame
from pygame import mixer
from time import time as timer

pygame.init()
mixer.init()
mixer.music.load('galaxy.mp3')
mixer.music.play()
fire_sound = mixer.Sound("Yellow SOUL shoot.wav")

font.init()
font2 = font.SysFont("Arial", 36)
win = font2.render("YOU WIN!", True, (51, 255, 0))
lose = font2.render("YOU LOSE!", True, (180, 0, 0))

score = 0 
lost = 0 

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

score = 0
goal = 30
lost = 0
max_lost = 5

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1 


class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_height = 500
win_width = 700

display.set_caption("Shooter")
FPS = 180
clock = time.Clock()

window = display.set_mode((win_width, win_height))
backround = transform.scale(image.load(img_back), (win_width , win_height))
ship = Player(img_hero, 5, 400, 80, 100, 10)

run = True 
finish = False
monsters = sprite.Group()
rel_time = False
life = 3
num_fire = 0

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(300, win_width - 30), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_z:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(backround,(0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.update()
        ship.update()
        bullets.update()
        display.update()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        ship.reset()

        if rel_time == True:
            now_Time = timer()

            if now_Time - last_time < 3:
                reload = font2.render("Reloading...", 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Score: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        life_color = (255, 255, 255)

        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)   

    time.delay(50)