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
size = 600

#buffer used to make sure everything is nicely on the screen
buffer = 10

#radius of the points
radius = buffer / 4

#used to determine size of rectangles(15% of screen size)
twentyPercent = size * .2

# creates the screen
screen = pygame.display.set_mode((size, size))

# caption for the screen
pygame.display.set_caption("(ESC: Clear Static) (Q: Start/Stop/Reset Moving) (Click & Release: Draw)")

# boolean run case
exit = False

#list of points
points = []

#creates all the points at random locations
for i in range(int((size // 100) * (size // 100) * 2.5)):
    points.append(Point(random.randint(buffer, size - buffer), random.randint(buffer, size - buffer), radius, screen, (0, 255, 0)))

#moving rec pointer
r = None

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

    if r != None:
        #draws the moving rectangle
        r.draw()
        #queries moving rec and stores result in query list
        qt.query(Rect((r.width / 2) + r.x, (r.height / 2) + r.y, r.width, r.height, screen), query)

    for event in pygame.event.get():

        # exits the game if x is clicked
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            p1 = pygame.mouse.get_pos()
        
        #places static rectangle on mouse click
        if event.type == pygame.MOUSEBUTTONUP:
            p2 = pygame.mouse.get_pos()
            
            #new instance of static rec
            if p1[0] <= p2[0] and p1[1] <= p2[1]:
                new_rec = Rectangle(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], screen, (255,0,255), False)
            elif p1[0] > p2[0] and p1[1] < p2[1]:
                new_rec = Rectangle(p2[0], p1[1], p1[0] - p2[0], p2[1] - p1[1], screen, (255,0,255), False)
            elif p1[0] > p2[0] and p1[1] > p2[1]:
                new_rec = Rectangle(p2[0], p2[1], p1[0] - p2[0], p1[1] - p2[1], screen, (255,0,255), False)
            else:
                new_rec = Rectangle(p1[0], p2[1], p2[0] - p1[0], p1[1] - p2[1], screen, (255,0,255), False)

            #queries the new static rectangle
            qt.query(Rect((new_rec.width / 2) + new_rec.x, (new_rec.height / 2) + new_rec.y, new_rec.width, new_rec.height, screen), still_query)

            #adds for redraw
            recs.append(new_rec)

        
        #clears all the static rectangles and static queries if esc is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                recs.clear()
                still_query.clear()

            if event.key == pygame.K_q:
                #moving rectangle
                if  r != None and r.Moves == False:
                    r = Rectangle(0, 0, twentyPercent, twentyPercent, screen, (255,255,0), True)
                elif r != None:
                    r = Rectangle(r.x, r.y, twentyPercent, twentyPercent, screen, (255,255,0), False)
                else:
                    r = Rectangle(0, 0, twentyPercent, twentyPercent, screen, (255,255,0), True)

        

    #draws all the points
    for point in points:
        point.color = (0, 255, 0)
        point.radius = radius
        
        #changes points in moving rec
        for p in query:
            if p.x == point.x and p.y == point.y:
                point.color = (0,255,255)
                point.radius = 4

        #changes points in still recs
        for p in still_query:
            if p.x == point.x and p.y == point.y:
                point.color = (0,255,255)
                point.radius = 4

        point.draw()

    #draws all the static rectangles
    for rec in recs:
        rec.draw()

    #option to see quad tree
    #qt.draw()

    #updates the screen
    pygame.display.flip()

    #set to 60FPS
    clock.tick(60)