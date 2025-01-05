import pygame

from main import *


class Priest(Hero):
    def spell(self):
        if self.spellRecharge <= 0 < self.health:
            self.health += 100
            if self.health > self.max_health:
                self.health = self.max_health
            self.spellRecharge = 120


class Dodger(Hero):
    def spell(self):
        if self.spellRecharge <= 0 < self.health:
            l = 50
            if pygame.key.get_pressed()[pygame.K_w]:
                for _ in range(l):
                    self.move_up()
            if pygame.key.get_pressed()[pygame.K_a]:
                for _ in range(l):
                    self.move_left()
            if pygame.key.get_pressed()[pygame.K_s]:
                for _ in range(l):
                    self.move_down()
            if pygame.key.get_pressed()[pygame.K_d]:
                for _ in range(l):
                    self.move_right()
            self.spellRecharge = 120


class Warrior(Hero):
    def spell(self):
        if self.spellRecharge <= 0 < self.health:
            pass
            self.spellRecharge = 120
