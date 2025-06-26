from canvas_elements import Line, Circle, GroundSymbol, Arrow, TripleCircle
from logic import state, switches
from logic import custom_switches

class synchrocheck:
    def __init__(self, canvas):
        self.canvas = canvas
        self.active = False
        self.elements = []

    def toggle(self):
        if self.active:
            self.deactivate()
        else:
            self.activate()

    def activate(self):
        if self.active:
            return
        self.active = True

        offset_x, offset_y = 0, 50
        spacing, shift_x = 150, -75

        from canvas_elements.line import Line
        from canvas_elements.TripleCircle import TripleCircle

        t1 = TripleCircle(self.canvas, center_x=460, center_y=55, spacing=10, circle_radius=16, line_width=3)
        t1.draw()
        self.elements.extend(t1.elements)

        self.elements.append(state.synchro_bus_id)

        self.elements.append(self.canvas.create_line(500 + offset_x + shift_x, -26 + offset_y,
                                                    200 + offset_x + spacing * 2 + shift_x, 20 + offset_y, width=2))
        self.elements.append(self.canvas.create_line(500 + offset_x + shift_x, -26 + offset_y,
                                                    235 + offset_x + spacing * 2 + shift_x, -26 + offset_y, width=2))
        self.elements.append(self.canvas.create_line(536 + offset_x + shift_x, -27 + offset_y,
                                                    235 + offset_x + spacing * 2 + shift_x, -20 + offset_y, width=2))

        t2 = TripleCircle(self.canvas, center_x=540, center_y=55, spacing=10, circle_radius=16, line_width=3)
        t2.draw()
        self.elements.extend(t2.elements)

        self.elements.append(self.canvas.create_line(650 + offset_x + shift_x, -26 + offset_y,
                                                    350 + offset_x + spacing * 2 + shift_x, 20 + offset_y, width=2))
        self.elements.append(self.canvas.create_line(616 + offset_x + shift_x, -26 + offset_y,
                                                    350 + offset_x + spacing * 2 + shift_x, -26 + offset_y, width=2))
        self.elements.append(self.canvas.create_line(616 + offset_x + shift_x, -27 + offset_y,
                                                    315 + offset_x + spacing * 2 + shift_x, -20 + offset_y, width=2))

    def deactivate(self):
        if not self.active:
            return
        for el in self.elements:
            self.canvas.delete(el)
        self.elements.clear()
        self.active = False
        ids_to_clear = [
            "synchro_bus_id",
            "synchro_bus_tail",
            "synchro_line_id",
            "synchro_line_tail",
            "synchro_bc_left",
            "synchro_bc_middle",
            "synchro_bc_right",
            "synchro_bridge"
        ]
        for name in ids_to_clear:
            item_id = getattr(state, name, None)
            if item_id:
                self.canvas.delete(item_id)
            setattr(state, name, None)

        self.active = False