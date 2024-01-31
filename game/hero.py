import pygame

class Hero:
    def __init__(self, x, y, width, height, step, color, bullet_size):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.step = step
        self.color = color
        self.bullet_size = bullet_size

    def draw(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

    def set_ammo(self):
        pass

    def new_bullet(self):
        return (self.x + self.w, self.y + self.h/2, self.bullet_size, self.bullet_size)