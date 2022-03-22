import pygame
from pygame.locals import *
import os.path
import random

#---------------------------------------------------------------------------------------------------------------------------------------------
# Zmienne globalne
#---------------------------------------------------------------------------------------------------------------------------------------------


width = 1000
height = 700
size = (width, height)
title = "GalaCats"
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 89, 214)


#---------------------------------------------------------------------------------------------------------------------------------------------
# Klasy i funkcje potrzebne do gry
#---------------------------------------------------------------------------------------------------------------------------------------------


def imgload(file):
    """ Funkcja ładuje obraz z pliku i przekształca go w powierzchnię okna gry """

    filepath = os.path.join("./stuff", file)
    img = pygame.image.load(filepath)  # wczytanie pliku na płaszczyznę
    img = img.convert() # konwersja na format pikseli ekranu
    img.set_colorkey(black)

    return img

def sndload(file):
    """ Funkcja ładuje dźwięk z pliku """
    filepath = os.path.join("stuff", file)
    sound = pygame.mixer.Sound(filepath)
    return sound


class GoodKitty(pygame.sprite.Sprite):
    """ Klasa reprezentująca postać gracza """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload("goodkitty.jpg")
        self.rect = self.image.get_rect() # rozmiar taki jak rozmiar załadowanego rysunku
        self.rect.center = (width/2, 0.8*height) 
        self.x_velocity = 0
        self.y_velocity = 0
        self.health = 9

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity)) 

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

class GoodLaser(pygame.sprite.Sprite):
    """ Klasa rezprezentująca pociski gracza """

    def __init__(self,startpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload("blue.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = startpos

    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip((0,-15))


class BadKitty(pygame.sprite.Sprite):
    """ Klasa reprezentująca podrzędnych wrogów """
  
    def __init__(self,startx):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload("badkitty.jpg")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = 300
        self.x_velocity = 0
        self.y_velocity = random.choice([i for i in range(-2,2) if i != 0])

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))
        self.x_velocity = self.x_velocity
        if self.rect.bottom < 250 or self.rect.bottom > 0.8*height:
            self.y_velocity = -(self.y_velocity)


class BossKitty(pygame.sprite.Sprite):
    """ Klasa reprezentująca wrogów, których pokonanie jest konieczne do ukończenia gry """
  
    def __init__(self,startx):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload("bosskitty.jpg")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = 60
        self.x_velocity = 4
        self.y_velocity = 0
        self.health = 9

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))
        self.y_velocity = self.y_velocity
        
        if self.rect.left < 0 or self.rect.right > width:
            self.x_velocity = -(self.x_velocity)
        


class BossLaser(pygame.sprite.Sprite):
    """ Klasa reprezentująca lasery wrogów """
  
    def __init__(self,startpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload("red.jpg")
        self.rect = self.image.get_rect()
        self.rect.midtop = startpos

    def update(self):
        if self.rect.bottom >= height:
            self.kill()
        else:
            self.rect.move_ip((0,15))



def get_high_score():
    """ Funkcja wczytująca najlepszy wynik z pliku .txt """
    
    if os.path.exists("stuff/highscore.txt"):
        scorefile = open("stuff/highscore.txt", "r")
        highscore = int(scorefile.read())
        scorefile.close()
        return highscore
    else:
        return 0


def save_high_score(newscore):
    """ Funkcja zapisująca najlepszy wynik do pliku .txt """
    
    scorefile = open("stuff/highscore.txt", "r")
    highscore = int(scorefile.read())
    scorefile.close()
    if newscore > highscore:
        scorefile = open("stuff/highscore.txt", "w")
        scorefile.write(str(newscore))
        scorefile.close()


def gameover(screen):
    """ Funkcja wyświetlająca okno przegranej gry """

    click = False
    while True:
        bkg = imgload("space.jpg")
        screen.fill(black)
        screen.blit(bkg, (0, 0))
        
        
        draw_text("GAME OVER", pygame.font.Font("stuff/Pokemon GB.ttf", 70), pink, screen, width/2, 100)

        button1 = Button(100, 500, 250, 50, "NEW GAME", pink, black)
        button1.draw(screen)
        button2 = Button(650, 500, 250, 50, "QUIT", pink, black)
        button2.draw(screen)

        if button1.check():
            if click:
                play(screen)
        if button2.check():
            if click:
                pygame.quit()
                quit()
        click = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()



def absolute_win(screen):
    """ Funkcja wyświetlająca okno ukończonej gry """

    click = False
    while True:
        bkg = imgload("space.jpg")
        screen.fill(black)
        screen.blit(bkg, (0, 0))
        
        
        draw_text("ABSOLUTE WIN", pygame.font.Font("stuff/Pokemon GB.ttf", 70), pink, screen, width/2, 100)

        button1 = Button(100, 500, 250, 50, "NEW GAME", pink, black)
        button1.draw(screen)
        button2 = Button(650, 500, 250, 50, "QUIT", pink, black)
        button2.draw(screen)

        if button1.check():
            if click:
                play(screen)
        if button2.check():
            if click:
                pygame.quit()
                quit()
        click = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()

    


def play(screen):
    """ Funkcja wywołująca grę """

    bkg = imgload("space.jpg")

    goodsound = sndload("goodlaser.wav")
    meow = sndload("meow.wav")
    scream = sndload("scream.wav")
    badsound = sndload("badlaser.wav")
    sad = sndload("sad.wav")
    purr = sndload("purr.wav")
    levelup = sndload("levelup.wav")

    level = 1
    score = 0 
    life_count = 9
    font = pygame.font.Font("stuff/Pokemon GB.ttf", 12)

    spritegood = pygame.sprite.Group()
    goodkitty = GoodKitty()
    spritegood.add(goodkitty)
    goodlasersprites = pygame.sprite.Group()


    badsprites = pygame.sprite.Group()
    for i in range(1,10):
        badsprites.add(BadKitty(100*i))

    boss_sprites = pygame.sprite.Group()
    boss_sprites.add(BossKitty(200))
    bosslasersprites = pygame.sprite.Group()


    clock = pygame.time.Clock()
    done = False
    while not done:
            clock.tick(50)
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            done = True
                        elif event.key == K_LEFT:
                            goodkitty.x_velocity = -8
                        elif event.key == K_RIGHT:
                            goodkitty.x_velocity = 8
                        elif event.key == K_SPACE:
                            goodlasersprites.add(GoodLaser(goodkitty.rect.midtop))
                            goodsound.play()
                        
                    elif event.type == KEYUP:
                        if event.key == K_LEFT:
                            goodkitty.x_velocity = 0 
                        elif event.key == K_RIGHT:
                            goodkitty.x_velocity = 0

            screen.fill(black)
            screen.blit(bkg, (0, 0))


            spritegood.update() # aktualizacja sprite'a
            goodlasersprites.update()
            badsprites.update()
            boss_sprites.update()
            bosslasersprites.update()

            for hit in pygame.sprite.groupcollide(badsprites, goodlasersprites, 1, 1):
                meow.play()
                score += 1

            for badkitty in badsprites:
                for goodkitty in spritegood:
                    if pygame.sprite.collide_rect(badkitty, goodkitty):
                        meow.play()
                        badkitty.kill()
                        life_count -= 1
                        goodkitty.health -= 1
                        break
                    if goodkitty.health == 0:
                        sad.play() 
                        goodkitty.kill()
                        gameover(screen)
                        


            for boss in boss_sprites:
                shoot = random.randint(1,70)
                if shoot == 1:
                    bosslasersprites.add(BossLaser(boss.rect.midbottom))
                    badsound.play()


            for laser in goodlasersprites:
                for bosskitty in boss_sprites:
                    if pygame.sprite.collide_rect(laser, bosskitty):
                        laser.kill()
                        score += 1
                        bosskitty.health -= 1
                        break
                    if bosskitty.health == 0:
                        scream.play()
                        bosskitty.kill()


            for laser in bosslasersprites:
                for goodkitty in spritegood:
                    if pygame.sprite.collide_rect(laser, goodkitty):
                        laser.kill()
                        life_count -= 1
                        goodkitty.health -= 1
                        break
                    if goodkitty.health == 0:
                        sad.play()
                        goodkitty.kill()
                        gameover(screen) 

            if not boss_sprites:
                levelup.play()
                life_count = 9
                level += 1
                badsprites.empty()
                for i in range(1, level+1):
                    boss_sprites.add(BossKitty(200*i))
                for i in range(1,10):
                    badsprites.add(BadKitty(100*i))
                if level > 3:
                    purr.play()
                    absolute_win(screen)
                

            spritegood.clear(screen, bkg) # czyszczenie tła
            goodlasersprites.clear(screen, bkg)
            badsprites.clear(screen, bkg)
            boss_sprites.clear(screen, bkg)
            bosslasersprites.clear(screen, bkg)

            
            spritegood.draw(screen) # rysowanie sprite'a
            goodlasersprites.draw(screen)
            badsprites.draw(screen)
            boss_sprites.draw(screen)
            bosslasersprites.draw(screen)

            text = font.render("SCORE: " + str(score), 1, pink)
            screen.blit(text, (20,670))
            text2 = font.render("LIFE COUNT: " + str(life_count), 1, pink)
            screen.blit(text2, (800,670))
            text3 = font.render(f"LEVEL: {level}", 1, pink)
            screen.blit(text3, (420,670))

            save_high_score(score)

            pygame.display.flip()


#---------------------------------------------------------------------------------------------------------------------------------------------
# Klasy i funkcje potrzebne do menu głównego
#---------------------------------------------------------------------------------------------------------------------------------------------


class Button(object):
    """ Klasa reprezentująca przycisk """
    def __init__(self, x, y, width, height, text, textcolor, backgroundcolor):
        object.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = textcolor
        self.background = backgroundcolor
        self.angle = 0
    def check(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self, screen):
        pygame.draw.rect(screen, self.background, (self.rect), 0)
        draw_text_center(self.text, pygame.font.Font("stuff/Pokemon GB.ttf", 20), screen, self.x+(self.width/2), self.y+(self.height/2), self.text_color)
        pygame.draw.rect(screen, self.text_color, self.rect, 5)

def draw_text_center(text, font, screen, x, y, color):
    """ Wpisanie tekstu na obiekt (przycisk) """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    screen.blit(textobj, textrect)

def draw_text(text, font, color, surface, x, y):
    """ Wpisanie tekstu w oknie pygame """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    surface.blit(textobj, textrect)

def rules(screen):
    """ Funkcja wyświetla okno z zasadami gry """
    click = False
    while True:
        bkg = imgload("space.jpg")
        screen.fill(black)
        screen.blit(bkg, (0, 0))
        
        rulesfile = open("stuff/rules.txt", "r") 
        lines = rulesfile.readlines() 
        rulesfile.close()

        count = 0
        for line in lines:
            count += 1
            draw_text(line, pygame.font.Font("stuff/Pokemon GB.ttf", 12), pink, screen, width/2, 50+40*count)

        button1 = Button(100, 600, 250, 50, "START GAME", pink, black)
        button1.draw(screen)
        button2 = Button(650, 600, 250, 50, "QUIT", pink, black)
        button2.draw(screen)

        if button1.check():
            if click:
                play(screen)
        if button2.check():
            if click:
                pygame.quit()
                quit()
        click = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        pygame.display.update()



def main_menu(screen):
    """ Funkcja wyświetla menu główne """
    click = False
    while True:
        bkg = imgload("space.jpg")
        screen.fill(black)
        screen.blit(bkg, (0, 0))
        draw_text("MAIN MENU", pygame.font.Font("stuff/Pokemon GB.ttf", 50), pink, screen, width/2, 50)
        draw_text("AUTHOR: ADA MAJCHRZAK", pygame.font.Font("stuff/Pokemon GB.ttf", 20), pink, screen, width/2, 150)
        draw_text(f"BEST SCORE: {get_high_score()}", pygame.font.Font("stuff/Pokemon GB.ttf", 20), pink, screen, width/2, 200)
        button1 = Button(width/2-130, 300, 250, 50, "GAME RULES", pink, black)
        button1.draw(screen)
        button2 = Button(width/2-130, 400, 250, 50, "START GAME", pink, black)
        button2.draw(screen)
        button3 = Button(width/2-130, 500, 250, 50, "QUIT", pink, black)
        button3.draw(screen)
        if button1.check():
            if click:
                rules(screen)
        if button2.check():
            if click:
                play(screen)
        if button3.check():
            if click:
                pygame.quit()
                quit()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


#---------------------------------------------------------------------------------------------------------------------------------------------
# Wywołanie programu
#---------------------------------------------------------------------------------------------------------------------------------------------


def main():
    pygame.init()
    screen = pygame.display.set_mode(size, 0, 0)
    pygame.display.set_caption(title)
    main_menu(screen)

if __name__ == "__main__":
    main()

