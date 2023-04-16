from time import time

import pygame
from math import *
from random import *

window = pygame.display.set_mode((400, 700))
background = pygame.image.load('ggg (1).jpg')
background = pygame.transform.scale(background, (400, 700))




# hp_image = pygame.image.load("hp1.png")
# hp_image = pygame.transform.scale(hp_image, (100, 30))
# hp_list = ["hp1.png", "hp2.png", "hp3.png", "hp4.png", "hp5.png", "hp6.png", "hp7.png", "hp8.png", "hp9.png",
#            "hp10.png", "hp11.png"]
# hp = 0
# explosion_list = ["exp00.png", "exp01.png", "exp02.png", "exp03.png", "exp04.png", "exp05.png", "exp06.png",
#                   "exp07.png", "exp08.png"]
# exp = 0
clock = pygame.time.Clock()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.width = width
        self.height = height

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Hero(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.x < 300:
            self.rect.x += self.speed
        elif keys[pygame.K_DOWN] and self.rect.y < 600:
            self.rect.y += self.speed
        elif keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            pygame.mixer.init()
            sound.play()
            self.image = pygame.transform.scale(pygame.image.load("spaceship1.png"), (self.width, self.height))

        else:
            sound.stop()
            self.image = pygame.transform.scale(pygame.image.load("spaceship3.png"), (self.width, self.height))

    def fire(self):
        bullet = Bullets("laser.png", player.rect.centerx - 15, player.rect.y - 30, 25, 70, 15, 15)
        bullet1 = Bullets("laser1.png", player.rect.x + 15, player.rect.y - 30, 20, 85, 15, 15)
        bullet2 = Bullets("laser1.png", player.rect.x + 60, player.rect.y - 30, 20, 85, 15, 15)
        bullets.add(bullet)
        bullets.add(bullet1)
        bullets.add(bullet2)
        bullet.image = pygame.transform.rotate(bullet.image, -45)
        bullet1.image = pygame.transform.rotate(bullet1.image, -45)
        bullet2.image = pygame.transform.rotate(bullet2.image, -45)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.height:
            self.kill()

    def shoot(self):
        fire = Bulletss("laser1 - Copy.png", self.rect.centerx - 15, self.rect.y + 50, 20, 70, 10, player.rect.x + 40,
                        player.rect.y + 20)
        bulletss.add(fire)
        angle = fire.location(fire.rect.x, fire.rect.y, player.rect.x, player.rect.y)
        fire = pygame.transform.rotate(fire.image, 90-angle)


class Bullets(GameSprite):
    def __init__(self,image, x, y, width, height, speed, speedx):
        super().__init__(image, x, y, width, height, speed)
        self.speedx = speedx

    def update(self):
        self.rect.y -= self.speed
        self.rect.x += self.speedx
        if self.rect.y < 0:
            self.kill()


class Bulletss(GameSprite):
    def __init__(self, image, x, y, width, height, speed, targetx, targety):
        super().__init__(image, x, y, width, height, speed)
        angle = atan2(targety - y, targetx - x)
        self.targetx = cos(angle)
        self.targety = sin(angle)

    def update(self):
        self.rect.y += self.targety * self.speed
        self.rect.x += self.targetx * self.speed
        if self.rect.y > 700:
            self.kill()

    def location(self, x, y, targetx, targety):
        dx = targetx - x
        dy = targety - y
        rad = atan2(dy, dx)
        rad = rad % (2 * pi)
        angle = degrees(rad)
        return angle



player = Hero('spaceship3.png', 150, 550, 100, 100, 5)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bulletss = pygame.sprite.Group()

pygame.mixer.init()
sound = pygame.mixer.Sound("sound.mp3")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()
sound2 = pygame.mixer.Sound("blaster.mp3")
explosion = pygame.mixer.Sound("explosion.mp3")

pygame.font.init()
font1 = pygame.font.SysFont(None, 30)
score_text = font1.render("score:", True, (255, 255, 255))
def gaming():
    hp_image = pygame.image.load("hp1.png")
    hp_image = pygame.transform.scale(hp_image, (100, 30))
    hp_list = ["hp1.png", "hp2.png", "hp3.png", "hp4.png", "hp5.png", "hp6.png", "hp7.png", "hp8.png", "hp9.png",
               "hp10.png", "hp11.png"]
    hp = 0
    explosion_list = ["exp00.png", "exp01.png", "exp02.png", "exp03.png", "exp04.png", "exp05.png", "exp06.png",
                      "exp07.png", "exp08.png"]
    exp = 0
    w = 0
    height = 700
    y = 0
    y1 = -height
    e = 0
    s = 0
    counter_score = 0
    game = True
    finish = False

    num_fire = 0
    reload_time = False

    while game:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if num_fire < 10 and reload_time == False:
                        num_fire += 1
                        player.fire()
                        sound2.play()
                        sound2.set_volume(0.2)
                    if num_fire >= 10 and reload_time == False:
                        start_time = time()
                        reload_time = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                player.fire()
                sound2.play()
                sound2.set_volume(0.2)

        if finish != True:
            y += 3
            window.blit(background, (0, y))
            y1 += 3
            window.blit(background, (0, y1))
            if y > height:
                y = -height
            if y1 > height:
                y1 = -height

            if w == 0:
                w = 80
                enemy = Enemy("eee.png", randint(5, 300), 0, 100, 100, randint(1, 3))
                enemies.add(enemy)
            else:
                w -= 2

            for e in enemies:
                if s == 0:
                    s = 40
                    e.shoot()
                else:
                    s -= 1

            player.show()
            player.move()
            enemies.draw(window)
            enemies.update()
            window.blit(hp_image, (0, 10))

            bullets.update()
            bullets.draw(window)


            bulletss.update()
            bulletss.draw(window)
            for b in bullets:
                if b.rect.x >= 400:
                    b.speedx *= -1
                    b.image = pygame.transform.rotate(b.image, 90)

            score_text = font1.render("Score:" + str(counter_score), True, (255, 255, 255))
            window.blit(score_text, (10, 50))

            # events = pygame.event.get()
            # for event in events:
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         if num_fire < 10 and reload_time == False:
                #             num_fire += 1
                #             player.fire()
                #             sound2.play()
                #             sound2.set_volume(0.2)
                #         if num_fire >=10 and reload_time == False:
                #             start_time = time()
                #             reload_time = True
                #
                # if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                #     player.fire()
                #     sound2.play()
                #     sound2.set_volume(0.2)

            if reload_time == True:
                end = time()
                if end - start_time >= 3:
                    reload_time = False
                    num_fire = 0
                else:
                    reload_text = font1.render('Reloading...', True, (255, 255, 255))
                    window.blit(reload_text, (160, 300))


            collides = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for collide in collides:
                counter_score += 1
                explosion.play()
                e = 0
                for i in range(9):
                    if e == 0:
                        e = 40
                        collide.image = pygame.transform.scale(pygame.image.load(explosion_list[i]), (100, 100))
                        window.blit(collide.image, (collide.rect.x, collide.rect.y))
                    else:
                        e -= 1

            if pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, bulletss, True):
                if hp == 10:
                    hp = 0
                else:
                    hp += 1
                hp_image = pygame.image.load(hp_list[hp])
                hp_image = pygame.transform.scale(hp_image, (100, 30))
                explosion.play()
                e = 0
                for i in range(9):
                    if e == 0:
                        e = 40
                        bulletss.image = pygame.transform.scale(pygame.image.load(explosion_list[i]), (100, 100))
                        window.blit(bulletss.image, (player.rect.x, player.rect.y))
                    else:
                        e -= 1
        if counter_score >= 4:
            finish = True

        if hp == 11:
            finish = True




        pygame.display.update()
        clock.tick(60)

menu = pygame.transform.scale(pygame.image.load('ggg (1).jpg'), (400, 700))
play = font1.render("PLAY(press any key)", True, (255, 255, 255))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        if event.type == pygame.KEYDOWN:
                gaming()
                run = False
    window.blit(menu, (0,0))
    window.blit(play, (160, 300))
    pygame.display.update()
    clock.tick(60)