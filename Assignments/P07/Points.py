import pygame

class Point():
    def __init__(self, x, y, radius, screen, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.color = color

    def draw(self):
        #draws the point
        pygame.draw.circle(
            self.screen, self.color, [self.x, self.y], self.radius)
