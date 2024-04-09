class Mountain:
    def __init__(self, height, radius, center):
        self.height = height
        self.radius = radius
        self.center = center

    def getX(self):
        return self.center[0]

    def getY(self):
        return self.center[1]