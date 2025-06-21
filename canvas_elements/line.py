class Line:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.line = canvas.create_line(x1, y1, x2, y2, width=2)
        self.start = (x1, y1)
        self.end = (x2, y2)

    def move(self, dx, dy):
        self.canvas.move(self.line, dx, dy)
