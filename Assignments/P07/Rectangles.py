import pygame

class Rectangle():
    def __init__(self, x, y, width, height, screen, color, Moves = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        self.Moves = Moves

    def draw(self):
        #if it doesn't move stay still
        if self.Moves == False:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 1)
        #if it moves move one unit to the right/move to the left side/stop
        else:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 1)

            #conditions for movement
            #go to left side        
            if self.x + self.width > self.screen.get_size()[0]:
                self.y += self.height
                self.x = 0
            #stop
            elif self.y >= self.screen.get_size()[0]:
                self.Moves = False
            #move one unit right
            else:
                self.x += 1
            