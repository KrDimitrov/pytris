import vmath
from math import isnan

BLOCK_SIZE = 30

def getAxes(points):
    axes = []
    for i, point in enumerate(points):
        p1 = vmath.Vector(*point)
        p2 = vmath.Vector(*points[0 if i+1 == len(points) else i+1])
        edge = vmath.subtract(p1, p2)
        axes.append(edge.normal()[0])
    return axes

def project(points, axis):
    dot = []
    for point in points:
        vec = vmath.Vector(*point)
        product = vmath.dotProduct(axis, vec)
        if isnan(product):
            raise Exception("Broken collision", f"dotProduct was NaN for vector:{vec} and axis: {axis} on point {point}")
        dot.append(product)
    dot.sort()
    return (dot[0], dot[-1])

def areOverlapping(proj1, proj2):
    return proj1[0] <= proj2[1] and proj1[1] >= proj2[0]

def getOverlapLength(proj1, proj2):
    if not areOverlapping(proj1, proj2): return 0.0
    return min(proj1[1], proj2[1]) - max(proj1[0], proj2[0])
    


def checkCollision(tetroA, tetroB):
    for polygonA in tetroA.polygons:
        for polygonB in tetroB.polygons:
            if (polygonA.pX < polygonB.pX + polygonB.width and
                polygonA.pX + polygonA.width > polygonB.pX and
                polygonA.pY < polygonB.pY + polygonB.height and
                polygonA.pY + polygonA.height > polygonB.pY):
                    tetroA.color = (255,0,0)
                    tetroB.color = (0, 0, 255)
                    return True

    return False
