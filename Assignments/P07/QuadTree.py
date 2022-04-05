import numpy as np
import random
import pygame
from Rectangles import Rectangle

class Point:
    """A point located at (x,y) in 2D space.
    Each Point object may be associated with a payload object.
    """

    def __init__(self, x, y, payload=None):
        self.x, self.y = x, y
        self.payload = payload

    def __repr__(self):
        return "{}: {}".format(str((self.x, self.y)), repr(self.payload))

    def __str__(self):
        return "P({:.2f}, {:.2f})".format(self.x, self.y)

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            other_x, other_y = other
        return np.hypot(self.x - other_x, self.y - other_y)


class Rect:
    """A rectangle centred at (cx, cy) with width w and height h."""

    def __init__(self, cx, cy, w, h, screen):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.west_edge, self.east_edge = cx - w / 2, cx + w / 2
        self.north_edge, self.south_edge = cy - h / 2, cy + h / 2
        self.screen = screen

    def __repr__(self):
        return str((self.west_edge, self.east_edge, self.north_edge, self.south_edge))

    def __str__(self):
        return "({:.2f}, {:.2f}, {:.2f}, {:.2f})".format(
            self.west_edge, self.north_edge, self.east_edge, self.south_edge
        )

    def contains(self, point):
        """Is point (a Point object or (x,y) tuple) inside this Rect?"""

        try:
            point_x, point_y = point.x, point.y
        except AttributeError:
            point_x, point_y = point

        return (
            point_x >= self.west_edge
            and point_x < self.east_edge
            and point_y >= self.north_edge
            and point_y < self.south_edge
        )

    def intersects(self, other):
        """Does Rect object other interesect this Rect?"""
        return not (
            other.west_edge > self.east_edge
            or other.east_edge < self.west_edge
            or other.north_edge > self.south_edge
            or other.south_edge < self.north_edge
        )

    def draw(self):
        rec = Rectangle(self.west_edge, self.north_edge, self.w, self.h, self.screen, (255, 0, 0))
        
        rec.draw()


class QuadTree:
    """A class implementing a quadtree."""

    def __init__(self, bbox, screen, max_points=4, depth=0):
        """Initialize this node of the quadtree.
        bbox is a Rect object defining the region from which points are
        placed into this node; max_points is the maximum number of points the
        node can hold before it must divide (branch into four more nodes);
        depth keeps track of how deep into the quadtree this node lies.
        """

        self.bbox = bbox
        self.max_points = max_points
        self.points = []
        self.depth = depth
        # A flag to indicate whether this node has divided (branched) or not.
        self.divided = False
        self.screen = screen

    def __str__(self):
        """Return a string representation of this node, suitably formatted."""
        sp = " " * self.depth * 2
        s = str(self.bbox) + "\n"
        s += sp + ", ".join(str(point) for point in self.points)
        if not self.divided:
            return s
        return (
            s
            + "\n"
            + "\n".join(
                [
                    sp + "nw: " + str(self.nw),
                    sp + "ne: " + str(self.ne),
                    sp + "se: " + str(self.se),
                    sp + "sw: " + str(self.sw),
                ]
            )
        )

    def divide(self):
        """Divide (branch) this node by spawning four children nodes."""

        cx, cy = self.bbox.cx, self.bbox.cy
        w, h = self.bbox.w / 2, self.bbox.h / 2
        # The boundaries of the four children nodes are "northwest",
        # "northeast", "southeast" and "southwest" quadrants within the
        # bbox of the current node.
        self.nw = QuadTree(
            Rect(cx - w / 2, cy - h / 2, w, h, self.screen), self.screen, self.max_points, self.depth + 1
        )
        self.ne = QuadTree(
            Rect(cx + w / 2, cy - h / 2, w, h, self.screen), self.screen, self.max_points, self.depth + 1
        )
        self.se = QuadTree(
            Rect(cx + w / 2, cy + h / 2, w, h, self.screen), self.screen, self.max_points, self.depth + 1
        )
        self.sw = QuadTree(
            Rect(cx - w / 2, cy + h / 2, w, h, self.screen), self.screen, self.max_points, self.depth + 1
        )
        self.divided = True

    def insert(self, point):
        """Try to insert Point point into this QuadTree."""

        if not self.bbox.contains(point):
            # The point does not lie inside bbox: bail.
            return False
        if len(self.points) < self.max_points:
            # There's room for our point without dividing the QuadTree.
            self.points.append(point)
            return True

        # No room: divide if necessary, then try the sub-quads.
        if not self.divided:
            self.divide()

        return (
            self.ne.insert(point)
            or self.nw.insert(point)
            or self.se.insert(point)
            or self.sw.insert(point)
        )

    def query(self, bbox, found_points):
        """Find the points in the quadtree that lie within bbox."""

        if not self.bbox.intersects(bbox):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within bbox ...
        for point in self.points:
            if bbox.contains(point):
                found_points.append(point)
        # ... and if this node has children, search them too.
        if self.divided:
            self.nw.query(bbox, found_points)
            self.ne.query(bbox, found_points)
            self.se.query(bbox, found_points)
            self.sw.query(bbox, found_points)
        return found_points

    def query_circle(self, bbox, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre.
        bbox is a Rect object (a square) that bounds the search circle.
        There is no need to call this method directly: use query_radius.
        """

        if not self.bbox.intersects(bbox):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within bbox
        # and also lie within a circle of given radius around the centre point.
        for point in self.points:
            if bbox.contains(point) and point.distance_to(centre) <= radius:
                found_points.append(point)

        # Recurse the search into this node's children.
        if self.divided:
            self.nw.query_circle(bbox, centre, radius, found_points)
            self.ne.query_circle(bbox, centre, radius, found_points)
            self.se.query_circle(bbox, centre, radius, found_points)
            self.sw.query_circle(bbox, centre, radius, found_points)
        return found_points

    def query_radius(self, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre."""

        # First find the square that bounds the search circle as a Rect object.
        bbox = Rect(*centre, 2 * radius, 2 * radius,self.screen)
        return self.query_circle(bbox, centre, radius, found_points)

    def __len__(self):
        """Return the number of points in the quadtree."""

        numpoints = len(self.points)
        if self.divided:
            numpoints += len(self.nw) + len(self.ne) + len(self.se) + len(self.sw)
        return numpoints

    def draw(self):
        """Draw a representation of the quadtree in pygame."""
        rec = Rectangle(self.bbox.west_edge, self.bbox.north_edge, self.bbox.w, self.bbox.h,self.screen, (255, 0, 0))
        
        rec.draw()
        
        if self.divided:
            self.nw.draw()
            self.ne.draw()
            self.se.draw()
            self.sw.draw()