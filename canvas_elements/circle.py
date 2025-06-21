class Circle:
    def __init__(self, canvas, x=100, y=100, r=20):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.circle = canvas.create_oval(
            x - r, y - r, x + r, y + r, width=2
        )

    def move(self, dx, dy):
        self.canvas.move(self.circle, dx, dy)
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.move(dx, dy)

    def set_radius(self, new_r):
        self.canvas.delete(self.circle)
        self.r = new_r
        self.circle = self.canvas.create_oval(
            self.x - new_r, self.y - new_r,
            self.x + new_r, self.y + new_r,
            width=2
        )
        