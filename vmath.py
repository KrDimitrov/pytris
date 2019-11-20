import math

class Vector:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def magnitude(self):
        return math.sqrt(self.posX*self.posX + self.posY * self.posY)

    def normalize(self):
        l = self.magnitude()
        if l==0:
            # null vector, cannot normalize
            return
        self.posX /= l
        self.posY /= l
    

def dotProduct(vecA, vecB):
    return vecA.posX * vecB.posX + vecA.posY * vecB.posY

def project(vecA, vecB):
    dp = dotProduct(vecA, vecB)
    lenSqr = pow(vecB.magnitude(), 2)
    return Vector(((dp/lenSqr)*vecB.posX), ((dp/lenSqr)*vecB.posY))
