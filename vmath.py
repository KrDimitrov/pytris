import math

class Vector:
    """A simple Vector class"""
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def __str__(self):
        return f"Vector: ({self.posX}, {self.posY}) length: {self.magnitude()}"
    def magnitude(self):
        """Returns the magnitude/length of the vector"""
        return math.sqrt(self.posX*self.posX + self.posY * self.posY)

    def normalize(self):
        l = self.magnitude()
        if l==0:
            # null vector, cannot normalize
            return
        self.posX /= l
        self.posY /= l
    
    def normal(self):
        return (Vector(-self.posY, self.posX), Vector(self.posY, -self.posX))

def dotProduct(vecA, vecB):
    return vecA.posX * vecB.posX + vecA.posY * vecB.posY

def project(vecA, vecB):
    dp = dotProduct(vecA, vecB)
    lenSqr = pow(vecB.magnitude(), 2)
    return Vector(((dp/lenSqr)*vecB.posX), ((dp/lenSqr)*vecB.posY))

def subtract(vecA, vecB):
    return Vector(vecA.posX - vecB.posX, vecA.posY - vecB.posY)
