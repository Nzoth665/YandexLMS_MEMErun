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
        self.shift = (xshift, yshift)
        self.limitation = (
            self.indentation + xshift, self.indentation + yshift, self.width - self.indentation + xshift,
            self.height - self.indentation + yshift)

    def render(self):
        self.screen.fill("#FF0000", (self.shift[0], self.shift[1], self.width, self.height))
        self.screen.fill("#00FF00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation))

    def clear(self):
        self.screen.fill("#00FF00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation))

    def item_inside(self, pos, hitbox):
        return self.limitation[0] < pos[0] and pos[0] + hitbox[0] < self.limitation[2] and self.limitation[1] < pos[
            1] and pos[1] + hitbox[1] < self.limitation[3]


class Entity:
    def __init__(self, speed, position, health, damage, hitbox, board):
        self.speed = speed
        self.position = position
        self.health = health
        self.damage = damage
        self.hitbox = hitbox
        self.board = board
        self.image = pygame.Surface([20, 20])
        self.image.fill(pygame.Color("red"))

    def set_image(self, image):
        self.image = load_image(image)

    def get_hit(self, damage):
        self.health -= damage

    def draw(self):
        screen.blit(self.image, self.position)

    # moves
    def move_up(self):
        if self.board.item_inside([self.position[0], self.position[1] - self.speed], self.hitbox):
            self.position[1] -= self.speed

    def move_right(self):
        if self.board.item_inside([self.position[0] + self.speed, self.position[1]], self.hitbox):
            self.position[0] += self.speed

    def move_down(self):
        if self.board.item_inside([self.position[0], self.position[1] + self.speed], self.hitbox):
            self.position[1] += self.speed

    def move_left(self):
        if self.board.item_inside([self.position[0] - self.speed, self.position[1]], self.hitbox):
            self.position[0] -= self.speed


class Hero(Entity):
    def __init__(self, speed, position, health, damage, board):
        super().__init__(speed, position, health, damage, (20, 20), board)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.move_up()
        if pygame.key.get_pressed()[pygame.K_a]:
            self.move_left()
        if pygame.key.get_pressed()[pygame.K_s]:
            self.move_down()
        if pygame.key.get_pressed()[pygame.K_d]:
            self.move_right()


wait_for = 0.5
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('game')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    board = Board(600, 600, 5, screen, 50, 50)
    hero = Hero(2, [100, 100], 10, 5, board)
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
