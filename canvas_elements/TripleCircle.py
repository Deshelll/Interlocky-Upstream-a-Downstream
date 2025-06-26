import math

class TripleCircle:
    def __init__(self, canvas, center_x=0, center_y=0, spacing=8, circle_radius=20, line_width=3):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.spacing = spacing
        self.circle_radius = circle_radius
        self.line_width = line_width
        self.elements = []

    def draw(self):
        self.clear()

        angles_deg = [270, 30, 150]
        for angle in angles_deg:
            rad = math.radians(angle)
            x = self.center_x + self.spacing * math.cos(rad)
            y = self.center_y + self.spacing * math.sin(rad)
            circle = self.canvas.create_oval(
                x - self.circle_radius, y - self.circle_radius,
                x + self.circle_radius, y + self.circle_radius,
                width=self.line_width,
                outline="black"
            )
            self.elements.append(circle)

    def clear(self):
        for el in self.elements:
            self.canvas.delete(el)
        self.elements.clear()

    def move_to(self, x, y):
        self.center_x = x
        self.center_y = y
        self.draw()

    def set_spacing(self, s):
        self.spacing = s
        self.draw()

    def set_circle_radius(self, r):
        self.circle_radius = r
        self.draw()

    def set_line_width(self, w):
        self.line_width = w
        self.draw()
