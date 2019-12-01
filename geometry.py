from typing import Tuple
import vmath

class Polygon:
    # rectangle "polygon"
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        self.pX, self.pY = position
        self.width, self.height = size
        self.points = [position, (self.pX+self.width, self.pY), (self.pX+self.width, self.pY+self.height), (self.pX, self.pY+self.height)]

    def rotate(self, rotationPoint: Tuple[int, int]):
        self.points = list(map(lambda point: (-(point[1] - rotationPoint[1]) + rotationPoint[0] , (point[0] - rotationPoint[0]) + rotationPoint[1]), self.points))
    
    # move the polygon by a vector.
    # aka move all the points of the polygon by a vector
    # alot of cunfision between Vectors and points. Couldve used a tuple with (x, y)???
    def move(self, vector: vmath.Vector):
        self.points = list(map(lambda point: (point[0]+vector.posX, point[1]+vector.posY),self.points))

    # returns the Points of the polygon.
    # also provides the option to return moved points by vector. 
    # does not effect the polygon. 
    def getPoints(self, vector=None):
        
        if vector is None:
            return self.points
        return list(map(lambda point: (point[0]+vector.posX, point[1]+vector.posY),self.points))



