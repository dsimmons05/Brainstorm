import math
import pygame
class Triangle:
    def __init__(self, surface, color, center, height, width, degrees):
        self.surface = surface
        self.color = color
        self.width = width
        self.center = center
        self.height = height
        self.x, self.y = self.center
        self.degrees = degrees
        x, y = self.center
        self.point, self.rtip, self.ltip = find_points(center, height, degrees, 0)   
        self.lst_points = [self.point, self.rtip, self.ltip] 
    def move(self, x, y, degrees):
        a, b = self.center
        self.x += x
        self.y += y
        self.center = (a + x, b + y)
        self.point, self.rtip, self.ltip = find_points(self.center, self.height, degrees, self.degrees)
        self.lst_points = [self.point, self.rtip, self.ltip]   
        self.degrees += degrees
        self.degrees %= 360
    def draw(self):
        pygame.draw.polygon(self.surface, self.color, self.lst_points, self.width)
    def align(self, point):  
        point_angle = [angle_find(self.center, point) - angle_find(self.point, point), self.point]
        if abs(point_angle[0]) < 1:
            if distance_to(self.point, point) > distance_to(self.center, point):
                self.move(0, 0, 4)        
        if abs(point_angle[0]) > 1:
            if angle_find(self.center, point) > angle_find(self.point, point):
                self.move(0, 0, -4)
            if angle_find(self.center, point) < angle_find(self.point, point): 
                self.move(0, 0, 4)

def find_points(center, height, degrees, current_degrees):
    '''Finds the points of a equilateral triangle given the center point and 
    height.'''
    x, y = center
    point = (x, y - height)
    ltip = (x - height, y + height)
    rtip = (x + height, y + height)
    x, y = point
    eye1 = (x - 50, y - 50)
    eye2 = (x + 50, y - 50)      
    degrees += current_degrees
    point = rotate_point(center, point, degrees)
    ltip = rotate_point(center, ltip, degrees)
    rtip = rotate_point(center, rtip, degrees)
    return (point, rtip, ltip)

def rotate_point(center, point, degrees):
    angle = degrees * math.pi / 180
    xdis = center[0]
    ydis = center[1]
    x0, y0 = (point[0] - xdis, point[1] - ydis)
    x_point = (x0 * math.cos(angle) - y0 * math.sin(angle))
    y_point = (x0 * math.sin(angle) + y0 * math.cos(angle))
    return (x_point + xdis, y_point + ydis)

def angle_find(rotpoint, point):
    xdis = rotpoint[0]
    ydis = rotpoint[1]
    rad = math.atan2(point[1] - ydis, point[0] - xdis)
    angle = rad * 180 / math.pi
    return angle

def unit_vector(opoint, dpoint):
    '''Finds the unit vector from the origin point to the destination point.'''
    ox, oy = opoint
    dx, dy = dpoint
    i = dx - ox
    j = dy - oy
    mag = distance_to(opoint, dpoint)
    return (i / mag, j / mag)
    
def distance_to(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
