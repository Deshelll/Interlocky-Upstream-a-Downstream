from canvas_elements import Line, Circle, GroundSymbol
from logic import state, switches
from logic import custom_switches

def draw_schematic(canvas):
    offset_x = 150  # регулируй по вкусу
    offset_y = 50

    # Верхняя линия питания
    Line(canvas, 0 + offset_x, 20 + offset_y, 400 + offset_x, 20 + offset_y)
    Line(canvas, 200 + offset_x, 20 + offset_y, 200 + offset_x, 80 + offset_y)
    Line(canvas, 130 + offset_x, 105 + offset_y, 180 + offset_x, 105 + offset_y)
    Line(canvas, 200 + offset_x, 180 + offset_y, 200 + offset_x, 155 + offset_y)
    Line(canvas, 200 + offset_x, 130 + offset_y, 200 + offset_x, 105 + offset_y)
    Circle(canvas, x=200 + offset_x, y=200 + offset_y, r=20)

    # Нижняя часть цепи
    Line(canvas, 0 + offset_x, 400 + offset_y, 400 + offset_x, 400 + offset_y)
    Line(canvas, 200 + offset_x, 400 + offset_y, 200 + offset_x, 340 + offset_y)
    Line(canvas, 130 + offset_x, 315 + offset_y, 180 + offset_x, 315 + offset_y)
    Line(canvas, 200 + offset_x, 315 + offset_y, 200 + offset_x, 285 + offset_y)
    Line(canvas, 200 + offset_x, 265 + offset_y, 200 + offset_x, 240 + offset_y)
    Circle(canvas, x=200 + offset_x, y=219 + offset_y, r=20)

    # Индикация напряжения
    canvas.create_text(250 + offset_x, 215 + offset_y, text="KUVAG NO VOLT", font=("Arial", 10), anchor="w")
    state.voltage_indicator = canvas.create_rectangle(370 + offset_x, 207 + offset_y, 390 + offset_x, 227 + offset_y, fill="green", outline="black")

    # Земля
    GroundSymbol(canvas, 130 + offset_x, 115 + offset_y)
    GroundSymbol(canvas, 130 + offset_x, 325 + offset_y)

    # === Переключатели и хитбоксы ===

    # Верхний переключатель
    state.switch_parts = []
    switch = canvas.create_line(180 + offset_x, 80 + offset_y, 200 + offset_x, 105 + offset_y, width=2)
    state.switch_parts.append(switch)
    canvas.tag_bind(switch, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))
    hitbox1 = canvas.create_rectangle(170 + offset_x, 70 + offset_y, 210 + offset_x, 110 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox1, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))

    # Нижний переключатель
    state.lower_switch_parts = []
    lower = canvas.create_line(180 + offset_x, 340 + offset_y, 200 + offset_x, 315 + offset_y, width=2)
    state.lower_switch_parts.append(lower)
    canvas.tag_bind(lower, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))
    hitbox2 = canvas.create_rectangle(170 + offset_x, 305 + offset_y, 210 + offset_x, 345 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox2, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))

    # Верхний средний
    state.middle_upper_parts = []
    upper_mid = canvas.create_line(180 + offset_x, 130 + offset_y, 200 + offset_x, 155 + offset_y, width=2)
    state.middle_upper_parts.append(upper_mid)
    canvas.tag_bind(upper_mid, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))
    hitbox3 = canvas.create_rectangle(170 + offset_x, 125 + offset_y, 210 + offset_x, 160 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox3, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))

    # Нижний средний
    state.middle_lower_parts = []
    lower_mid = canvas.create_line(180 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y, width=2)
    state.middle_lower_parts.append(lower_mid)
    canvas.tag_bind(lower_mid, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))
    hitbox4 = canvas.create_rectangle(170 + offset_x, 255 + offset_y, 210 + offset_x, 290 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox4, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))


def draw_schematic_task2(canvas):
    offset_x = 0
    offset_y = 50
    spacing = 150
    shift_x = -75  # сдвиг всей схемы влево

    # === ВЕРХНЯЯ ГОРИЗОНТАЛЬНАЯ ШИНА ===
    Line(canvas, 200 + offset_x + shift_x, 20 + offset_y, 200 + offset_x + spacing * 2 + shift_x, 20 + offset_y)

    # === ВТОРАЯ ГОРИЗОНТАЛЬНАЯ ШИНА (НИЖНЯЯ) ===
    second_busbar_start_x = 200 + spacing * 3 + shift_x
    second_busbar_y = 20 + offset_y
    Line(canvas, second_busbar_start_x, second_busbar_y, second_busbar_start_x + spacing * 2, second_busbar_y)

    # === ШКАФ 1 ===
    draw_branch_frame(canvas, dx=offset_x + shift_x, dy=offset_y)  # только фон и линии
    custom_switches.register_three_switch(canvas, x=200 + offset_x + shift_x, y=105 + offset_y, group_id="cabinet1")
    custom_switches.register_two_switch(canvas, x=200 + offset_x + shift_x, y=155 + offset_y, group_id="cabinet1")

    # === ШКАФ 2 ===
    draw_custom_branch_shaft_2(canvas, dx=offset_x + spacing + shift_x, dy=offset_y)

    # === ШКАФ 3–4 (двойной независимый) ===
    # === ЛЕВАЯ ЧАСТЬ БОЛЬШОГО ШКАФА (шкаф 3) ===
    draw_custom_branch_3_left(canvas, dx=spacing * 2 + shift_x, dy=offset_y)

    # === ПРАВАЯ ЧАСТЬ БОЛЬШОГО ШКАФА (шкаф 4) ===
    draw_custom_branch_3_right(canvas, dx=spacing * 2 + shift_x + 150, dy=offset_y)

    # === Горизонтальная линия между ними ===
    Line(canvas, 200 + spacing * 2 + shift_x, 180 + offset_y + 80,
         200 + spacing * 2 + shift_x + 150, 180 + offset_y + 80)

    # === ШКАФ 4 ===
    draw_custom_branch_4(canvas, dx=spacing * 4 + shift_x, dy=offset_y)

    # === ШКАФ 5 ===
    draw_custom_branch_5(canvas, dx=spacing * 5 + shift_x, dy=offset_y)


def draw_custom_branch_shaft_2(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4

    # === Общая геометрия ===

    # Вход сверху
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    # Горизонталь к верхнему выключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # Связь от верхнего к нижнему
    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)

    # Вертикаль вниз от нижнего
    Line(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension)

    # === Переключатели ===

    # Верхний трёхпозиционный
    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet2")

    # Нижний двухпозиционный
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet2")

def draw_custom_branch_3_left(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4

    # Вход сверху
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    # Горизонталь к верхнему выключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # От верхнего к нижнему
    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)

    # От нижнего вниз
    Line(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension)

    # Переключатели
    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet3")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet3")

def draw_custom_branch_3_right(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4

    # Вход сверху
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    # Горизонталь к переключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # От трёхпозиционника вниз
    Line(canvas, base_x, 105 + dy, base_x, 180 + dy + vertical_extension)

    # Переключатель
    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet3")

def draw_custom_branch_4(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4

    # Вход сверху
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    # Горизонталь к верхнему выключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # Линия от верхнего к нижнему
    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)

    # Линия от нижнего вниз
    Line(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension)

    # Переключатели
    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet4")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet4")

def draw_custom_branch_5(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4

    # Вход сверху
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    # Горизонталь к верхнему переключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # Соединение верхний → нижний → вниз
    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)
    Line(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension)

    # Переключатели
    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet5")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet5")

def draw_branch_frame(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70

    # Вертикаль от шины
    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)
    # Линия от верхнего переключателя к нижнему
    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)

    # Линия от нижнего переключателя вниз
    Line(canvas, base_x, 155 + dy, base_x, 155 + dy + 20 * 4)
    # Горизонталь к верхнему выключателю
    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)

    # Земля
    GroundSymbol(canvas, ground_x, 115 + dy)

    # Общая вертикаль вниз
    Line(canvas, base_x, 180 + dy, base_x, 180 + dy + 20 * 4)