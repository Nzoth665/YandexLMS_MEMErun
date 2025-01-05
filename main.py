import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
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
        self.screen.fill("#B22222", (self.shift[0], self.shift[1], self.width, self.height)) # кирпичный
        self.screen.fill("#FFCC00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation)) # цвет Яндекс

    def clear(self):
        self.screen.fill("#FFCC00", (
            self.indentation + self.shift[0], self.indentation + self.shift[1], self.width - 2 * self.indentation,
            self.height - 2 * self.indentation))

    def item_inside(self, pos, hitbox):
        return self.limitation[0] < pos[0] and pos[0] + hitbox[0] < self.limitation[2] and self.limitation[1] < pos[
            1] and pos[1] + hitbox[1] < self.limitation[3]


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, position, health, damage, hitbox, board, image, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(image), (40, 40))
        #self.image.fill(pygame.Color("red"))
        self.speed = speed
        # self.position = position
        self.health = health
        self.damage = damage
        #self.hitbox = hitbox
        self.board = board

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def set_image(self, image):
        self.image = load_image(image)

    def get_hit(self, damage):
        self.health -= damage

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # moves
    def move_up(self):
        if self.board.item_inside([self.rect.x, self.rect.y - self.speed], (self.rect.width, self.rect.height)):
            self.rect.y -= self.speed

    def move_right(self):
        if self.board.item_inside([self.rect.x + self.speed, self.rect.y], (self.rect.width, self.rect.height)):
            self.rect.x += self.speed

    def move_down(self):
        if self.board.item_inside([self.rect.x, self.rect.y + self.speed], (self.rect.width, self.rect.height)):
            self.rect.y += self.speed

    def move_left(self):
        if self.board.item_inside([self.rect.x - self.speed, self.rect.y], (self.rect.width, self.rect.height)):
            self.rect.x -= self.speed


class Hero(Entity):
    def __init__(self, speed, position, health, damage, board, *group):
        super().__init__(speed, position, health, damage, (20, 20), board, "hero.png", *group)

    def update(self):
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
    pygame.display.set_caption('MEMErun')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    board = Board(600, 600, 10, screen, 50, 50)
    hero = Hero(2, [100, 100], 10, 5, board, all_sprites)
    board.render()

    clc = pygame.time.Clock()
    to_go = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        board.clear()
        all_sprites.draw(screen)

        pygame.display.flip()
        clc.tick(120)
    pygame.quit()
