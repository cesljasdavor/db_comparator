class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({1}, {2})".format(str(self.x), str(self.y))
