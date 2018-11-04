class RelationalCoordinate(object):
    def __init__(self, x, y, id=None):
        self.x = x
        self.y = y
        self.id = id

    def __str__(self):
        return "RelationalCoordinate(id={0}, x={1}, y={2})".format(str(self.id), str(self.x), str(self.y))
