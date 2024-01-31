import pygame
import random

class Enemy:
    def __init__(self, x, y, size, hp_multiplier):
        self.x = x
        self.y = y
        self.size = size
        self.destroyed = False
        self.errante = random.random() < 0.3
        if self.errante:
            self.color = pygame.Color("green")
            self.base_hp = hp_multiplier * size**2 / 4
            self.current_hp = hp_multiplier * size**2 / 4
        else:
            self.color = pygame.Color("blue")
            self.base_hp = hp_multiplier * size**2
            self.current_hp = hp_multiplier * size**2
        self.follow_strategy = 1
        self.hero_collision = False
        self.left_screen = False

    def move(self, speed, hero_x, hero_y, hero_w, hero_h):
        factor = 1 if not self.errante else 1.5
        speed = speed * factor
        self.x = self.x - speed
        # if self.errante:
        #     if random.random() > 0.96:
        #         self.follow_strategy *= -1
        #     hero_direction = self.follow_strategy if hero_y > self.y else -self.follow_strategy
        #     self.y = self.y + hero_direction * speed

        if hero_x <= self.x <= hero_x + hero_w or hero_x <= self.x + self.size <= hero_x + hero_w:
            if hero_y <= self.y <= hero_y + hero_h or hero_y <= self.y + self.size <= hero_y + hero_h:
                self.hero_collision = True

        if self.x + self.size < 0:
            self.left_screen = True

    def shift_y(self, step):
        self.y = self.y + step

    def update_hp(self, damage):
        print(f"asteroid hit, HP {self.current_hp}/{self.base_hp}")
        self.current_hp -= damage
        if self.current_hp <= 0.1*self.base_hp:
            self.color = pygame.Color("red")
        elif self.current_hp <= 0.3*self.base_hp:
            self.color = pygame.Color("orange")
        elif self.current_hp <= 0.5*self.base_hp:
            self.color = pygame.Color("yellow")
        if self.current_hp < 0:
            self.destroyed = True

    def draw(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.size, self.size))
        # pygame.draw.circle(display, self.color, (self.x, self.y), self.size)
