class DbcomParser(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.points = None

    def parse(self):
        with open(self.file_name, "r") as file:
            lines = file.readlines()
            self.points = []
            for line in lines:
                data = line.strip().split(',')
                x = float(data[0])
                y = float(data[1])

                self.points.append((x, y))
