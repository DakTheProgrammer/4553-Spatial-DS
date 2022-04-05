import pygame
from Points import Point
from Rectangles import Rectangle
from QuadTree import QuadTree, Rect
from QuadTree import Point as Poi
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
radius = buffer / 4

#used to determine size of rectangles(15% of screen size)
fifteenPercent = size * .15

# creates the screen
screen = pygame.display.set_mode((size, size))

# caption for the screen
pygame.display.set_caption("Quad Tree Project (ESC: Clear Static Rectangles)")

# boolean run case
exit = False

#list of points
points = []

#creates all the points at random locations
for i in range(100):
    points.append(Point(random.randint(buffer, size - buffer), random.randint(buffer, size - buffer), radius, screen, (0, 0, 255)))

#moving rectangle
r = Rectangle(0, 0, fifteenPercent, fifteenPercent, screen, (255,0,0), True)

#list of static rectangles
recs = []

#The QuadTree
qt = QuadTree(Rect(size/2, size/2, size, size, screen), screen)

#adds points to the QuadTree
for point in points:
    qt.insert(Poi(point.x, point.y))

#holds query of all the still rectangles
still_query = []

while not exit:
    #clears the screen
    screen.fill((0, 0, 0))

    #holds query of moving rectangle
    query = []

    #queries moving rec and stores result in query list
    qt.query(Rect((r.width / 2) + r.x, (r.height / 2) + r.y, r.width, r.height, screen), query)

    for event in pygame.event.get():

        # exits the game if x is clicked
        if event.type == pygame.QUIT:
            exit = True
        
        #places static rectangle on mouse click
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            #new instance of static rec
            new_rec = Rectangle(pos[0] - fifteenPercent / 2, pos[1] - fifteenPercent / 2, fifteenPercent, fifteenPercent, screen, (255,0,0), False)
            
            #queries the new static rectangle
            qt.query(Rect((new_rec.width / 2) + new_rec.x, (new_rec.height / 2) + new_rec.y, new_rec.width, new_rec.height, screen), still_query)

            #adds for redraw
            recs.append(new_rec)

        
        #clears all the static rectangles and static queries if esc is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                recs.clear()
                still_query.clear()
        

    #draws all the points
    for point in points:
        point.color = (0, 0, 255)
        
        #changes points in moving rec
        for p in query:
            if p.x == point.x and p.y == point.y:
                point.color = (0,255,255)

        #changes points in still recs
        for p in still_query:
            if p.x == point.x and p.y == point.y:
                point.color = (0,255,255)

        point.draw()

    #draws all the static rectangles
    for rec in recs:
        rec.draw()

    #draws the moving rectangle
    r.draw()

    #option to see quad tree
    #qt.draw()

    #updates the screen
    pygame.display.flip()

    #set to 60FPS
    clock.tick(60)