class GroundSymbol:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.parts = []

        self.parts.append(canvas.create_line(x, y - 10, x, y + 5, width=2))

        self.parts.append(canvas.create_line(x - 7, y + 5, x + 7, y + 5, width=2))
        self.parts.append(canvas.create_line(x - 5, y + 9, x + 5, y + 9, width=2))
        self.parts.append(canvas.create_line(x - 3, y + 13, x + 3, y + 13, width=2))

    def move(self, dx, dy):
        for part in self.parts:
            self.canvas.move(part, dx, dy)
