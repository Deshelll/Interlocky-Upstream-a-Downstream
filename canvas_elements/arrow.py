import math
from .line import Line

class Arrow(Line):
    # Можно подстроить эти значения здесь
    offset_x = -0.4
    offset_y = 0

    def __init__(self, canvas, x1, y1, x2, y2, direction="up"):
        super().__init__(canvas, x1, y1, x2, y2)

        if direction == "up":
            self.arrowhead = self._draw_arrowhead(x1 + self.offset_x, y1 + self.offset_y + 68, upward=True)
        elif direction == "down":
            self.arrowhead = self._draw_arrowhead(x2 + self.offset_x, y2 + self.offset_y - 20, upward=False)

    def _draw_arrowhead(self, x, y, upward=True):
        angle = math.radians(20)     # угол между стрелкой и вертикалью
        length = 20                  # длина стрелки

        dx = length * math.sin(angle)
        dy = length * math.cos(angle)

        if upward:
            left = (x - dx, y + dy)
            right = (x + dx, y + dy)
        else:
            left = (x - dx, y - dy)
            right = (x + dx, y - dy)

        l1 = self.canvas.create_line(x - 1, y, *left, width=2)
        l2 = self.canvas.create_line(x, y, *right, width=2)

        return [l1, l2]

    def move(self, dx, dy):
        super().move(dx, dy)
        for part in self.arrowhead:
            self.canvas.move(part, dx, dy)
