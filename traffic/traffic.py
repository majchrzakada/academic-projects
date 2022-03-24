import numpy as np
import time
import pygame
import threading
import sys
import os
from PIL import Image
import glob
import matplotlib.pyplot as plt


# ---------- GUI - oprawa graficzna ----------

black = (0, 0, 0)
white = (255, 255, 255)


def imgload(file):
    """
    Function to load images on pygame window

    Args:
        file (str): image file name
    """
    filepath = os.path.join("./stuff", file)
    img = pygame.image.load(filepath)
    img = img.convert()
    transparent = white
    img.set_colorkey(transparent)
    return img


def draw_text_center(text, font, screen, x, y, color):
    """
    Function to draw centered text on pygame window

    Args:
        text (str): text to be displayed
        font: pygame font
        screen: pygame window
        x (int): x coordinate
        y (int): y coordinate
        color (tuple of ints): text color in RGB scale
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    screen.blit(textobj, textrect)


def draw_text(text, font, color, screen, x, y):
    """
       Function to draw text on pygame window

       Args:
           text (str): text to be displayed
           font: pygame font
           screen: pygame window
           x (int): x coordinate
           y (int): y coordinate
           color (tuple of ints): text color in RGB scale
       """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    screen.blit(textobj, textrect)


class Button(object):
    """
    Class representing button in pygame window

    Args:
        x (int): x coordinate
        y (int): y coordinate
        width (int): button width
        height (int): button height
        text (str): text to be displayed on the button
        textcolor (tuple of ints): text color in RGB scale
        backgroundcolor (tuple of ints): button color in RGB scale
    """
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

    def check(self):
        """
        Function to check if cursor collides with button
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen):
        """
        Function to draw buttons on pygame window

        Args:
             screen: pygame window
        """
        pygame.draw.rect(screen, self.background, self.rect, 0)
        draw_text_center(self.text, pygame.font.Font("stuff/Pokemon GB.ttf", 20), screen, self.x + int(self.width / 2),
                         self.y + int(self.height / 2), self.text_color)
        pygame.draw.rect(screen, self.text_color, self.rect, 5)


def main_menu(screen, num=0, analysis=False):
    """
    Function to display simulation's main menu

    Args:
        screen: pygame window
        num (int): number of simulation
        analysis (bool): flag to determine whether to plot data or not
    """
    click = False
    while True:
        bkg = imgload("menu.png")
        screen.blit(bkg, (0, 0))
        draw_text("MAIN MENU", pygame.font.Font("stuff/Pokemon GB.ttf", 50), white, screen, int(s_width / 2), 50)
        draw_text(f"Red light duration: {def_red}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 140)
        draw_text(f"Yellow light duration: {def_yellow}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 170)
        draw_text(f"Green light duration for directions in group 0: {green0}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 200)
        draw_text(f"Green light duration for directions in group 1: {green1}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 230)
        draw_text(f"Green light duration for directions in group 2: {green2}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 260)
        draw_text(f"Green light duration for directions in group 3: {green3}",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 290)
        draw_text("Info:",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 340)
        draw_text("During simulation press V to turn recording on/off",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 370)
        draw_text("To change parameters press QUIT and start again",
                  pygame.font.Font("stuff/Pokemon GB.ttf", 15), white, screen, int(s_width / 2), 400)
        disp_button = Button(int(s_width / 2) - 210, s_height - 160, 420, 50, "DISPLAY SIMULATION", white, black)
        disp_button.draw(screen)
        quit_button = Button(int(s_width / 2) - 210, s_height - 80, 420, 50, "QUIT", white, black)
        quit_button.draw(screen)
        if disp_button.check():
            if click:
                play(screen, num, analysis)
        if quit_button.check():
            if click:
                sys.exit()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


# ---------- SYGNALIZACJA ŚWIETLNA ----------

sign_coods = {0: [(312, 600), (312, 288), (696, 288), (816, 288)],
              1: [(192, 456), (192, 288), (576, 288), (792, 144)],
              2: [(192, 144), (576, 144), (912, 144)],
              3: [(312, 144), (696, 144)]}  # współrzędne sygnalizatorów

# parametry zadawane przez użytkownika (czas palenia się świateł):

def_red = int(input("Red light duration: "))
def_yellow = int(input("Yellow light duration: "))
green0 = int(input("Green light duration for group 0: "))
green1 = int(input("Green light duration for group 1: "))
green2 = int(input("Green light duration for group 2: "))
green3 = int(input("Green light duration for group 3: "))

# pogrupowanie sygnalizatorów ze względu na kolejność zapalania się zielonego światła:

signals = {0: {'sigs': [], 'green': green0}, 1: {'sigs': [], 'green': green1},
           2: {'sigs': [], 'green': green2}, 3: {'sigs': [], 'green': green3}}

# zmienne globalne (początkowe parametry świateł):

cur_green = 0
next_green = (cur_green + 1) % 4
cur_yellow = 0


class Signal:
    """
    Class representing traffic signals

    Args:
        red (int): red light duration
        yellow (int): yellow light duration
        green (int): green light duration
    """
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green


def sign_update():
    """
    Function to update traffic signals
    """
    for i in range(4):
        if i == cur_green:
            if cur_yellow == 0:
                for s in signals[i]['sigs']:
                    s.green -= 1
            else:
                for s in signals[i]['sigs']:
                    s.yellow -= 1
        else:
            for s in signals[i]['sigs']:
                s.red -= 1


def repeat():
    """
    Function to repeat traffic signals cycle
    """
    global cur_green, cur_yellow, next_green
    while signals[cur_green]['sigs'][0].green > 0:
        sign_update()
        time.sleep(1)
    cur_yellow = 1
    cur_dirs = dir_nums[cur_green]
    for d in cur_dirs:
        cur_cars = cars[d]
        for car in cur_cars[0]:
            car.stop = stoplines[d]
    while signals[cur_green]['sigs'][0].yellow > 0:
        sign_update()
        time.sleep(1)
    cur_yellow = 0

    for s in signals[cur_green]['sigs']:
        s.green = signals[cur_green]['green']
        s.yellow = def_yellow
        s.red = def_red

    cur_green = next_green
    next_green = (cur_green + 1) % 4

    for n in signals[next_green]['sigs']:
        for c in signals[cur_green]['sigs']:
            n.red = c.yellow + c.green
    repeat()


def initialize_signals():
    """
    Function to initialize traffic signals
    """
    sig1 = Signal(0, def_yellow, green0)
    signals[0]['sigs'].append(sig1)
    sig3 = Signal(0, def_yellow, green0)
    signals[0]['sigs'].append(sig3)
    sig7 = Signal(0, def_yellow, green0)
    signals[0]['sigs'].append(sig7)
    sig11 = Signal(0, def_yellow, green0)
    signals[0]['sigs'].append(sig11)

    sig2 = Signal(sig1.yellow + sig1.green, def_yellow, green1)
    signals[1]['sigs'].append(sig2)
    sig4 = Signal(sig1.yellow + sig1.green, def_yellow, green1)
    signals[1]['sigs'].append(sig4)
    sig8 = Signal(sig1.yellow + sig1.green, def_yellow, green1)
    signals[1]['sigs'].append(sig8)
    sig12 = Signal(sig1.yellow + sig1.green, def_yellow, green1)
    signals[1]['sigs'].append(sig12)

    sig5 = Signal(def_red, def_yellow, green2)
    signals[2]['sigs'].append(sig5)
    sig9 = Signal(def_red, def_yellow, green2)
    signals[2]['sigs'].append(sig9)
    sig13 = Signal(def_red, def_yellow, green2)
    signals[2]['sigs'].append(sig13)

    sig6 = Signal(def_red, def_yellow, green3)
    signals[3]['sigs'].append(sig6)
    sig10 = Signal(def_red, def_yellow, green3)
    signals[3]['sigs'].append(sig10)
    repeat()


# ---------- POJAZDY ----------

# długości ulic:
lens = {'t1': 6, 't2': 11, 't3': 11, 't4': 10, 't5': 9, 't6': 14, 't7': 19, 't8': 14, 't9': 9,
        't10': 7, 't11': 7, 't12': 9, 't13': 5, 'out1': 10, 'out2': 10, 'out3': 9, 'out4': 9,
        'out5': 9, 'out6': 5, 'out7': 19, 'out8': 6}

# początkowe współrzędne pojazdów:
startx = {'lamb1': 276, 'lamb2': 660, 'lamb3': 996, 'lamb4': 12, 'lamb5': 252, 'lamb6': 636, 'lamb7': 852}
starty = {'lamb1': 708, 'lamb2': 708, 'lamb3': 228, 'lamb4': 252, 'lamb5': 12, 'lamb6': 12, 'lamb7': 12}

# każdy kierunek jazdy ma przyporządkowaną listę aktualnie poruszających się samochodów oraz nr światła zielonego:
cars = {'t1': {0: [], 'green': 0}, 't2': {0: [], 'green': 1}, 't3': {0: [], 'green': 0},
        't4': {0: [], 'green': 1}, 't5': {0: [], 'green': 2}, 't6': {0: [], 'green': 3},
        't7': {0: [], 'green': 0}, 't8': {0: [], 'green': 1}, 't9': {0: [], 'green': 2},
        't10': {0: [], 'green': 3}, 't11': {0: [], 'green': 0}, 't12': {0: [], 'green': 1},
        't13': {0: [], 'green': 2}, 'out1': {0: [], 'green': 0 or 1 or 2 or 3},
        'out2': {0: [], 'green': 0 or 1 or 2 or 3}, 'out3': {0: [], 'green': 0 or 1 or 2 or 3},
        'out4': {0: [], 'green': 0 or 1 or 2 or 3}, 'out5': {0: [], 'green': 0 or 1 or 2 or 3},
        'out6': {0: [], 'green': 0 or 1 or 2 or 3}, 'out7': {0: [], 'green': 0 or 1 or 2 or 3},
        'out8': {0: [], 'green': 0 or 1 or 2 or 3}}

# ponowne przyporządkowanie kierunków jazdy do nr światła zielonego (dla ułatwienia - inne odwołanie):
dir_nums = {0: ['t1', 't3', 't7', 't11'], 1: ['t2', 't4', 't8', 't12'],
            2: ['t5', 't9', 't13'], 3: ['t6', 't10']}

# kolory samochodów:
colors = ['red', 'blue', 'green', 'purple', 'white']

# obrazki dla każdego koloru i kierunku jazdy:
dir_imgs = {'red': {'t1': 'carup.png', 't2': 'cardown.png', 't3': 'carup.png', 't4': 'carright.png',
                    't5': 'cardown.png', 't6': 'carleft.png', 't7': 'carup.png', 't8': 'carright.png',
                    't9': 'cardown.png', 't10': 'carleft.png', 't11': 'carright.png', 't12': 'cardown.png',
                    't13': 'carleft.png', 'out1': 'carleft.png', 'out2': 'carleft.png', 'out3': 'carup.png',
                    'out4': 'carup.png', 'out5': 'carup.png', 'out6': 'carright.png', 'out7': 'cardown.png',
                    'out8': 'cardown.png'},
            'blue': {'t1': 'bcarup.png', 't2': 'bcardown.png', 't3': 'bcarup.png', 't4': 'bcarright.png',
                     't5': 'bcardown.png', 't6': 'bcarleft.png', 't7': 'bcarup.png', 't8': 'bcarright.png',
                     't9': 'bcardown.png', 't10': 'bcarleft.png', 't11': 'bcarright.png', 't12': 'bcardown.png',
                     't13': 'bcarleft.png', 'out1': 'bcarleft.png', 'out2': 'bcarleft.png', 'out3': 'bcarup.png',
                     'out4': 'bcarup.png', 'out5': 'bcarup.png', 'out6': 'bcarright.png', 'out7': 'bcardown.png',
                     'out8': 'bcardown.png'},
            'green': {'t1': 'gcarup.png', 't2': 'gcardown.png', 't3': 'gcarup.png', 't4': 'gcarright.png',
                      't5': 'gcardown.png', 't6': 'gcarleft.png', 't7': 'gcarup.png', 't8': 'gcarright.png',
                      't9': 'gcardown.png', 't10': 'gcarleft.png', 't11': 'gcarright.png', 't12': 'gcardown.png',
                      't13': 'gcarleft.png', 'out1': 'gcarleft.png', 'out2': 'gcarleft.png', 'out3': 'gcarup.png',
                      'out4': 'gcarup.png', 'out5': 'gcarup.png', 'out6': 'gcarright.png', 'out7': 'gcardown.png',
                      'out8': 'gcardown.png'},
            'purple': {'t1': 'pcarup.png', 't2': 'pcardown.png', 't3': 'pcarup.png', 't4': 'pcarright.png',
                       't5': 'pcardown.png', 't6': 'pcarleft.png', 't7': 'pcarup.png', 't8': 'pcarright.png',
                       't9': 'pcardown.png', 't10': 'pcarleft.png', 't11': 'pcarright.png', 't12': 'pcardown.png',
                       't13': 'pcarleft.png', 'out1': 'pcarleft.png', 'out2': 'pcarleft.png', 'out3': 'pcarup.png',
                       'out4': 'pcarup.png', 'out5': 'pcarup.png', 'out6': 'pcarright.png', 'out7': 'pcardown.png',
                       'out8': 'pcardown.png'},
            'white': {'t1': 'wcarup.png', 't2': 'wcardown.png', 't3': 'wcarup.png', 't4': 'wcarright.png',
                      't5': 'wcardown.png', 't6': 'wcarleft.png', 't7': 'wcarup.png', 't8': 'wcarright.png',
                      't9': 'wcardown.png', 't10': 'wcarleft.png', 't11': 'wcarright.png', 't12': 'wcardown.png',
                      't13': 'wcarleft.png', 'out1': 'wcarleft.png', 'out2': 'wcarleft.png', 'out3': 'wcarup.png',
                      'out4': 'wcarup.png', 'out5': 'wcarup.png', 'out6': 'wcarright.png', 'out7': 'wcardown.png',
                      'out8': 'wcardown.png'}}

# pogrupowanie kierunków t_i, i=1,2,...13 oraz out_j, j=1,2,...,8 ze względu na stronę, w którą poruszają się samochody:
right = ['t4', 't8', 't11', 'out6']
left = ['t6', 't10', 't13', 'out1', 'out2']
up = ['t1', 't3', 't7', 'out3', 'out4', 'out5']
down = ['t2', 't5', 't9', 't12', 'out7', 'out8']

# linie zatrzymania przed skrzyżowaniem dla każdego kierunku jazdy:
stoplines = {'t1': 588, 't2': 516, 't3': 276, 't4': 228, 't5': 204, 't6': 300, 't7': 276,
             't8': 612, 't9': 204, 't10': 684, 't11': 828, 't12': 204, 't13': 900,
             'out1': 0, 'out2': 0, 'out3': 0, 'out4': 0, 'out5': 0, 'out6': 1008, 'out7': 720, 'out8': 720}

# będziemy sprawdzać ilość samochodów na kolejnych ulicach po każdej aktualizacji układu
jams = {'t1': [], 't2': [], 't3': [], 't4': [], 't5': [], 't6': [], 't7': [], 't8': [], 't9': [],
        't10': [], 't11': [], 't12': [], 't13': []}

# będziemy zliczać samochody opuszczające mapę kolejnymi wyjazdami
outs = {'out1': 0, 'out2': 0, 'out3': 0, 'out4': 0, 'out5': 0, 'out6': 0, 'out7': 0, 'out8': 0}


def prob(direction):
    """
    Function to choose in which direction should car go next

    Args:
        direction (str): car's current direction
    Returns:
        car's next direction (str)
    """
    if direction == 't1':
        directions = ['out1', 't3']
        probs = [1 / 2, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't2':
        directions = ['out1', 'out8']
        probs = [1 / 2, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't3':
        directions = ['out2', 'out3', 't8']
        probs = [1 / 4, 1 / 4, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't4':
        directions = ['out3', 't2', 't8']
        probs = [1 / 4, 1 / 4, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't5':
        directions = ['out2', 't2', 't8']
        probs = [1 / 2, 1 / 4, 1 / 4]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't6':
        directions = ['out3', 'out2', 't2']
        probs = [1 / 4, 1 / 2, 1 / 4]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't7':
        directions = ['t6', 'out4', 't11']
        probs = [1 / 4, 1 / 2, 1 / 4]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't8':
        directions = ['out7', 't11', 'out4']
        probs = [1 / 4, 1 / 4, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't9':
        directions = ['t6', 'out7', 't11']
        probs = [1 / 4, 1 / 2, 1 / 4]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't10':
        directions = ['out4', 't6', 'out7']
        probs = [1 / 4, 1 / 4, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't11':
        directions = ['out5', 'out6']
        probs = [1 / 2, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't12':
        directions = ['t10', 'out6']
        probs = [1 / 2, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction == 't13':
        directions = ['t10', 'out5']
        probs = [1 / 2, 1 / 2]
        return np.random.choice(directions, 1, p=probs)[0]
    elif direction in ['out1', 'out2', 'out3', 'out4', 'out5', 'out6', 'out7', 'out8']:
        return direction


class Car(pygame.sprite.Sprite):
    """
    Class representing car

    Args:
        direction (str): initial direction
        entry (str): entry through which car enters the map
        color (str): car color
    """
    def __init__(self, direction, entry, color):
        pygame.sprite.Sprite.__init__(self)

        self.direction = direction
        self.entry = entry
        self.x = startx[entry]
        self.y = starty[entry]
        self.color = color
        self.image = imgload(dir_imgs[self.color][self.direction])
        carlist = cars[direction][0]
        self.index = len(carlist) - 1
        if self.direction in right:
            self.stop = stoplines[self.direction] - self.index * 24
        elif self.direction in left:
            self.stop = stoplines[self.direction] + self.index * 24
        elif self.direction in down:
            self.stop = stoplines[self.direction] - self.index * 24
        elif self.direction in up:
            self.stop = stoplines[self.direction] + self.index * 24

    def update(self):
        """
        Function to update car's coordinates
        """
        if self.direction in right and self.direction != 'out6':
            if cur_green != cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] - self.index * 24
                if self.x < self.stop:
                    self.x += 24

            if self.x == stoplines[self.direction]:
                turn = prob(self.direction)
                if turn in up and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.x += 48
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.y -= 48
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24
                elif turn in right and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.x += 72
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24
                elif turn in down and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.x += 24
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.y += 24
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24

            elif cur_green == cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] - self.index * 24
                if self.x < self.stop:
                    self.x += 24

        elif self.direction == 'out6':
            if self.x > 1008:
                outs[self.direction] += 1
                carlist = cars[self.direction][0]
                self.kill()
                if len(carlist) > 0:
                    carlist.pop(0)
            else:
                self.x += 24

        elif self.direction in left and self.direction not in ['out1', 'out2']:
            if cur_green != cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] + self.index * 24
                if self.x > self.stop:
                    self.x -= 24

            if self.x == stoplines[self.direction]:
                turn = prob(self.direction)
                if turn in down and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.x -= 48
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.y += 48
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24
                elif turn in left and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.x -= 72
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24
                elif turn in up and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.x -= 24
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.y -= 24
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24

            elif cur_green == cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] + self.index * 24
                if self.x > self.stop:
                    self.x -= 24

        elif self.direction in ['out1', 'out2']:
            if self.x < 0:
                outs[self.direction] += 1
                carlist = cars[self.direction][0]
                self.kill()
                if len(carlist) > 0:
                    carlist.pop(0)
            else:
                self.x -= 24

        elif self.direction in down and self.direction not in ['out7', 'out8']:
            if cur_green != cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] - self.index * 24
                if self.y < self.stop:
                    self.y += 24

            if self.y == stoplines[self.direction]:
                turn = prob(self.direction)
                if turn in left and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y += 24
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.x -= 24
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24
                elif turn in down and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y += 72
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24
                elif turn in right and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y += 48
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.x += 48
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24

            elif cur_green == cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] - self.index * 24
                if self.y < self.stop:
                    self.y += 24

        elif self.direction in ['out7', 'out8']:
            if self.y > 720:
                outs[self.direction] += 1
                carlist = cars[self.direction][0]
                self.kill()
                if len(carlist) > 0:
                    carlist.pop(0)
            else:
                self.y += 24

        elif self.direction in up and self.direction not in ['out3', 'out4', 'out5']:
            if cur_green != cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] + self.index * 24
                if self.y > self.stop:
                    self.y -= 24

            if self.y == stoplines[self.direction]:
                turn = prob(self.direction)
                if turn in left and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y -= 48
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.x -= 48
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24
                elif turn in up and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y -= 72
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] + self.index * 24
                elif turn in right and cur_green == cars[self.direction]['green'] and len(cars[turn][0]) < lens[turn]:
                    self.y -= 24
                    self.image = imgload(dir_imgs[self.color][turn])
                    self.x += 24
                    carlist = cars[self.direction][0]
                    carlist.remove(self)
                    self.direction = turn
                    new_carlist = cars[self.direction][0]
                    new_carlist.append(self)
                    self.index = new_carlist.index(self)
                    self.stop = stoplines[self.direction] - self.index * 24

            elif cur_green == cars[self.direction]['green']:
                carlist = cars[self.direction][0]
                self.index = carlist.index(self)
                self.stop = stoplines[self.direction] + self.index * 24
                if self.y > self.stop:
                    self.y -= 24

        elif self.direction in ['out3', 'out4', 'out5']:
            if self.y < 0:
                outs[self.direction] += 1
                carlist = cars[self.direction][0]
                self.kill()
                if len(carlist) > 0:
                    carlist.pop(0)
            else:
                self.y -= 24


# ---------- NIEJEDNORODNY PROCES POISSONA ----------

# intensywności procesu Poissona dla kolejnych wjazdów na mapę:
lamb1 = lambda t: 0.8 + 0.8 * np.sin(t / 2)
lamb2 = lambda t: np.exp((2 * np.sin(t / 12 + 3) - 0.9) ** 3)
lamb3 = lambda t: 0.5
lamb4 = lambda t: 0.7 + 0.6 * ((np.sin(t / 7 + 2)) ** 2) * np.cos(t / 3 + 1)
lamb5 = lambda t: 0.2 + 0.2 * np.sign(np.sin(t / 24 + 6))
lamb6 = lambda t: 0.1 + 0.1 * np.sin(np.sqrt(t))
lamb7 = lambda t: 0.3 + 0.3 * np.sin(4 * np.sin(t / 2))

# globalne maksima każdej intensywności:
max1 = 1.6
max2 = 3.78483
max3 = 0.5
max4 = 1.3
max5 = 0.4
max6 = 0.2
max7 = 0.6


# --------------- SYMULACJA -------------------

def play(screen, num=0, analysis=False):
    """
    Function to display simulation on pygame window

    Args:
         screen: pygame window
         num (int): number of simulation
         analysis (bool): flag to determine whether to plot data or not
    """

    traffic = pygame.sprite.Group()

    thread1 = threading.Thread(name="initialization", target=initialize_signals, args=())
    thread1.daemon = True
    thread1.start()

    bkg = imgload("board.png")
    redsig = imgload('red.png')
    yellsig = imgload('yellow.png')
    greensig = imgload('green.png')

    clock = pygame.time.Clock()
    loop = True
    video = False
    img_num = 0  # licznik do zapisywania zrzutów ekranu
    folder = './gif'
    if len(os.listdir(folder)) != 0:   # jeśli mamy już zapisaną animację, usuwamy ją
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            os.unlink(path)

    # poczekalnie dla samochdów:
    l1_wait = []
    l2_wait = []
    l3_wait = []
    l4_wait = []
    l5_wait = []
    l6_wait = []
    l7_wait = []

    start1 = start2 = start3 = start4 = start5 = start6 = start7 = time.time()  # czas początkowy dla procesu Poissona

    while loop:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                if len(os.listdir(folder)) != 0:
                    frames = []
                    imgs = glob.glob('./gif/*.png')
                    for img in imgs:
                        frame = Image.open(img)
                        frames.append(frame)
                    frames[0].save('./gif/traffic.gif', format='GIF', append_images=frames[1:],
                                   save_all=True, duration=100, loop=0)
                    for file in os.listdir(folder):
                        path = os.path.join(folder, file)
                        if path.endswith('.png'):
                            os.remove(path)  # po stworzeniu animacji usuwamy zrzuty ekranu

                if analysis:
                    jam_list = [sum(jams[i]) / len(jams[i]) for i in jams.keys()]
                    plt.bar(list(range(13)), jam_list)
                    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], jams.keys())
                    plt.title(f'Średnie zakorkowanie ulic dla zestawu {num}', fontsize=10)
                    plt.xlabel("Numer ulicy")
                    plt.ylabel("Liczba samochodów na kratkę")
                    plt.savefig(f'./plots/jams{num}')
                    plt.clf()

                    out_list = [outs[i] for i in outs.keys()]
                    plt.bar(list(range(8)), out_list)
                    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], outs.keys())
                    plt.title(f'Liczba samochodów opuszczających mapę kolejnymi wyjazdami dla zestawu {num}', fontsize=10)
                    plt.xlabel("Numer wyjazdu")
                    plt.ylabel("Liczba samochodów")
                    plt.savefig(f'./plots/outs{num}')

                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:  # uruchamiamy nagrywanie naciskając V
                video = not video

        screen.blit(bkg, (0, 0))
        for i in range(4):
            cur_coods = sign_coods[i]
            if i == cur_green:
                if cur_yellow == 1:
                    for j in range(len(cur_coods)):
                        screen.blit(yellsig, cur_coods[j])
                else:
                    for j in range(len(cur_coods)):
                        screen.blit(greensig, cur_coods[j])
            else:
                for j in range(len(cur_coods)):
                    screen.blit(redsig, cur_coods[j])

        # dodawanie samochodów na mapę zgodnie z niejednorodnym procesem Poissona:
        u1_1 = np.random.rand()
        t1 = -(1 / max1) * np.log(u1_1)
        u1_2 = np.random.rand()
        if u1_2 <= lamb1(t1) / max1:
            if time.time() - start1 >= t1:
                col1 = np.random.choice(colors)
                l1_wait.append(Car('t1', 'lamb1', col1))
                if len(cars['t1'][0]) < lens['t1'] and len(l1_wait) > 0:
                    c1 = l1_wait.pop(0)
                    cars['t1'][0].append(c1)
                    traffic.add(c1)
                start1 = time.time()

        u2_1 = np.random.rand()
        t2 = -(1 / max2) * np.log(u2_1)
        u2_2 = np.random.rand()
        if u2_2 <= lamb2(t2) / max2:
            if time.time() - start2 >= t2:
                col2 = np.random.choice(colors)
                l2_wait.append(Car('t7', 'lamb2', col2))
                if len(cars['t7'][0]) < lens['t7'] and len(l2_wait) > 0:
                    c2 = l2_wait.pop(0)
                    cars['t7'][0].append(c2)
                    traffic.add(c2)
                start2 = time.time()

        u3_1 = np.random.rand()
        t3 = -(1 / max3) * np.log(u3_1)
        u3_2 = np.random.rand()
        if u3_2 <= lamb1(t3) / max3:
            if time.time() - start3 >= t3:
                col3 = np.random.choice(colors)
                l3_wait.append(Car('t13', 'lamb3', col3))
                if len(cars['t13'][0]) < lens['t13'] and len(l3_wait) > 0:
                    c3 = l3_wait.pop(0)
                    cars['t13'][0].append(c3)
                    traffic.add(c3)
                start3 = time.time()

        u4_1 = np.random.rand()
        t4 = -(1 / max4) * np.log(u4_1)
        u4_2 = np.random.rand()
        if u4_2 <= lamb3(t4) / max4:
            if time.time() - start4 >= t4:
                col4 = np.random.choice(colors)
                l4_wait.append(Car('t4', 'lamb4', col4))
                if len(cars['t4'][0]) < lens['t4'] and len(l4_wait) > 0:
                    c4 = l4_wait.pop(0)
                    cars['t4'][0].append(c4)
                    traffic.add(c4)
                start4 = time.time()

        u5_1 = np.random.rand()
        t5 = -(1 / max5) * np.log(u5_1)
        u5_2 = np.random.rand()
        if u5_2 <= lamb5(t5) / max5:
            if time.time() - start5 >= t5:
                col5 = np.random.choice(colors)
                l5_wait.append(Car('t5', 'lamb5', col5))
                if len(cars['t5'][0]) < lens['t5'] and len(l5_wait) > 0:
                    c5 = l5_wait.pop(0)
                    cars['t5'][0].append(c5)
                    traffic.add(c5)
                start5 = time.time()

        u6_1 = np.random.rand()
        t6 = -(1 / max6) * np.log(u6_1)
        u6_2 = np.random.rand()
        if u6_2 <= lamb6(t6) / max6:
            if time.time() - start6 >= t6:
                col6 = np.random.choice(colors)
                l6_wait.append(Car('t9', 'lamb6', col6))
                if len(cars['t9'][0]) < lens['t9'] and len(l6_wait) > 0:
                    c6 = l6_wait.pop(0)
                    cars['t9'][0].append(c6)
                    traffic.add(c6)
                start6 = time.time()

        u7_1 = np.random.rand()
        t7 = -(1 / max7) * np.log(u7_1)
        u7_2 = np.random.rand()
        if u7_2 <= lamb7(t7) / max7:
            if time.time() - start7 >= t7:
                col7 = np.random.choice(colors)
                l7_wait.append(Car('t12', 'lamb7', col7))
                if len(cars['t12'][0]) < lens['t12'] and len(l7_wait) > 0:
                    c7 = l7_wait.pop(0)
                    cars['t12'][0].append(c7)
                    traffic.add(c7)
                start7 = time.time()

        for car in traffic:
            car.update()
            screen.blit(car.image, (car.x, car.y))

        pygame.display.flip()

        if video:
            filename = str(img_num) + '.png'
            pygame.image.save(screen, f'./gif/{filename}')
            img_num += 1

        for direction in cars.keys():
            if direction in jams.keys():
                jams[direction].append(len(cars[direction][0]) / lens[direction])


if __name__ == '__main__':
    s_width = 1008
    s_height = 720
    size = (s_width, s_height)
    pygame.init()
    simulation_screen = pygame.display.set_mode(size, 0, 0)
    pygame.display.set_caption('Traffic simulation')
    main_menu(simulation_screen)
