class SwitchSymbol:
    def __init__(self, canvas, x, y, direction="right"):
        self.canvas = canvas
        self.parts = []
        offset = 10
        if direction == "right":
            self.parts.append(canvas.create_line(x, y, x+offset, y+offset, width=2))
            self.parts.append(canvas.create_line(x+offset, y+offset, x+offset*2, y, width=2))
        elif direction == "left":
            self.parts.append(canvas.create_line(x, y, x-offset, y+offset, width=2))
            self.parts.append(canvas.create_line(x-offset, y+offset, x-offset*2, y, width=2))

    def move(self, dx, dy):
        for item in self.parts:
            self.canvas.move(item, dx, dy)