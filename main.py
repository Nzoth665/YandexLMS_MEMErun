import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height, indentation, screen, xshift, yshift):
        self.size = self.width, self.height = width, height
        self.indentation = indentation
        self.screen = screen
        self.limitation = (
            self.indentation, self.indentation, self.width - 2 * self.indentation, self.height - 2 * self.indentation)
        self.shift = (xshift, yshift)

    def render(self):
        self.screen.fill("#FF0000", (self.shift[0], self.shift[1], self.width, self.height))
        self.screen.fill("#00FF00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation))

    def clear(self):
        self.screen.fill("#00FF00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation))

    def item_inside(self, coords):
        return (self.limitation[0], self.limitation[1]) < coords < (self.limitation[2], self.limitation[3])


class Entity:
    def __init__(self, speed, position, health, damage):
        self.speed = speed
        self.position = position
        self.health = health
        self.damage = damage
        self.image = pygame.Surface([20, 20])
        self.image.fill(pygame.Color("red"))

    def set_image(self, image):
        self.image = load_image(image)

    def get_hit(self, damage):
        self.health -= damage

    def draw(self):
        screen.blit(self.image, self.position)


class Hero(Entity):
    def __init__(self, speed, position, health, damage):
        super().__init__(speed, position, health, damage)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.position[1] -= self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            self.position[0] -= self.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.position[1] += self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.position[0] += self.speed


wait_for = 0.5
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('game')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    hero = Hero(2, [0, 0], 10, 5)
    board = Board(600, 600, 5, screen, 50, 50)
    board.render()

    clc = pygame.time.Clock()
    to_go = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        hero.move()
        board.clear()
        hero.draw()
        pygame.display.flip()
        clc.tick(120)
    pygame.quit()
