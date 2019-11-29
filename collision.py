import vmath

def getAxes(points):
    axes = []
    for i in range(0, len(points)):
        p1 = vmath.Vector(*points[i])
        p2 = vmath.Vector(*points[0 if i+1 == len(points) else i+1])
        edge = vmath.subtract(p1, p2)
        axes.append(edge.normal()[0])
    return axes

def project(points, axis):
    dot = []
    for point in points:
        vec = vmath.Vector(*point)
        dot.append(vmath.dotProduct(axis, vec))
    dot.sort()
    return (dot[0], dot[-1])

def checkCollision(pointsA, pointsB):
    axesA = getAxes(pointsA)
    axesB = getAxes(pointsB)

    for axis in axesA:
        p1 = project(pointsA, axis)
        p2 = project(pointsB, axis)

        if p2[1] < p1[0] or p1[1] < p2[0]:
            return False
    for axis in axesB:
        p1 = project(pointsA, axis)
        p2 = project(pointsB, axis)

        if p2[1] < p1[0] or p1[1] < p2[0]:
            return False
    return True
