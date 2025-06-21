class Coil:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.coil1 = canvas.create_oval(x-20, y-20, x+20, y+20, width=2)
        self.coil2 = canvas.create_oval(x-15, y-15, x+15, y+15, width=2)

    def move(self, dx, dy):
        self.canvas.move(self.coil1, dx, dy)
        self.canvas.move(self.coil2, dx, dy)