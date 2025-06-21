from canvas_elements import Line, Circle, GroundSymbol
from logic import state, switches

def draw_schematic(canvas):
    # Верхняя линия питания
    Line(canvas, 0, 20, 400, 20)
    Line(canvas, 200, 20, 200, 80)
    Line(canvas, 130, 105, 180, 105)
    Line(canvas, 200, 180, 200, 155)
    Line(canvas, 200, 130, 200, 105)
    Circle(canvas, x=200, y=200, r=20)

    # Нижняя часть цепи
    Line(canvas, 0, 400, 400, 400)
    Line(canvas, 200, 400, 200, 340)
    Line(canvas, 130, 315, 180, 315)
    Line(canvas, 200, 315, 200, 285)
    Line(canvas, 200, 265, 200, 240)
    Circle(canvas, x=200, y=219, r=20)

    # Индикация напряжения
    canvas.create_text(250, 215, text="KUVAG NO VOLT", font=("Arial", 10), anchor="w")
    state.voltage_indicator = canvas.create_rectangle(370, 207, 390, 227, fill="green", outline="black")

    # Земля
    GroundSymbol(canvas, 130, 115)
    GroundSymbol(canvas, 130, 325)

    # === Переключатели и хитбоксы ===

    # Верхний переключатель
    state.switch_parts = []
    switch = canvas.create_line(180, 80, 200, 105, width=2)
    state.switch_parts.append(switch)
    canvas.tag_bind(switch, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))
    hitbox1 = canvas.create_rectangle(170, 70, 210, 110, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox1, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))

    # Нижний переключатель
    state.lower_switch_parts = []
    lower = canvas.create_line(180, 340, 200, 315, width=2)
    state.lower_switch_parts.append(lower)
    canvas.tag_bind(lower, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))
    hitbox2 = canvas.create_rectangle(170, 305, 210, 345, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox2, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))

    # Верхний средний
    state.middle_upper_parts = []
    upper_mid = canvas.create_line(180, 130, 200, 155, width=2)
    state.middle_upper_parts.append(upper_mid)
    canvas.tag_bind(upper_mid, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))
    hitbox3 = canvas.create_rectangle(170, 125, 210, 160, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox3, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))

    # Нижний средний
    state.middle_lower_parts = []
    lower_mid = canvas.create_line(180, 286, 200, 261, width=2)
    state.middle_lower_parts.append(lower_mid)
    canvas.tag_bind(lower_mid, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))
    hitbox4 = canvas.create_rectangle(170, 255, 210, 290, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox4, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))
