import pygame
from Points import Point
from Rectangles import Rectangle
import random

# initializes the pygame instance
pygame.init()

#clock used for frames per second
clock = pygame.time.Clock()

#size of screen(square)
size = 500

#buffer used to make sure everything is nicely on the screen
buffer = 10

#radius of the points
radius = buffer / 2

#used to determine size of rectangles(15% of screen size)
fifteenPercent = size * .15

# creates the screen
screen = pygame.display.set_mode((size, size))

# caption for the screen
pygame.display.set_caption("Quad Tree Project (ESC: Clear Static Rectangles)")

# boolean run case
exit = False

points = []

#creates all the points at random locations
for i in range(10):
    points.append(Point(random.randint(buffer, size - buffer),
                        random.randint(buffer, size - buffer),
                        radius, screen, (255, 0, 0)))

#moving rectangle
r = Rectangle(0, 0, fifteenPercent, fifteenPercent, screen, (0,0,255), True)

#list of static rectangles
recs = []

while not exit:
    #clears the screen
    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        # exits the game if x is clicked
        if event.type == pygame.QUIT:
            exit = True
        
        #places static rectangle on mouse click
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            recs.append(Rectangle(pos[0] - fifteenPercent / 2,
                                  pos[1] - fifteenPercent / 2, fifteenPercent,
                                  fifteenPercent, screen, (0,0,255), False))
        
        #clears all the static rectangles if esc is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                recs.clear()

    #draws all the points
    for point in points:
        point.draw()

    #draws all the static rectangles
    for rec in recs:
        rec.draw()

    #draws the moving rectangle
    r.draw()

    #updates the screen
    pygame.display.flip()

    #set to 60FPS
    clock.tick(60)