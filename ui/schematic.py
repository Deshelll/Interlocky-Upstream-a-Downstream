from canvas_elements import Line, Circle, GroundSymbol, Arrow, TripleCircle
from logic import state, switches
from logic import custom_switches
from logic import state
from logic.custom_switches import draw_cross

def draw_schematic(canvas):
    offset_x = 150
    offset_y = 50


    Line(canvas, 0 + offset_x, 20 + offset_y, 400 + offset_x, 20 + offset_y)
    Line(canvas, 200 + offset_x, 20 + offset_y, 200 + offset_x, 80 + offset_y)
    Line(canvas, 130 + offset_x, 105 + offset_y, 180 + offset_x, 105 + offset_y)
    Line(canvas, 200 + offset_x, 180 + offset_y, 200 + offset_x, 155 + offset_y)
    Line(canvas, 200 + offset_x, 130 + offset_y, 200 + offset_x, 105 + offset_y)
    Circle(canvas, x=200 + offset_x, y=200 + offset_y, r=20)


    Line(canvas, 0 + offset_x, 400 + offset_y, 400 + offset_x, 400 + offset_y)
    Line(canvas, 200 + offset_x, 400 + offset_y, 200 + offset_x, 340 + offset_y)
    Line(canvas, 130 + offset_x, 315 + offset_y, 180 + offset_x, 315 + offset_y)
    Line(canvas, 200 + offset_x, 315 + offset_y, 200 + offset_x, 285 + offset_y)
    Line(canvas, 200 + offset_x, 265 + offset_y, 200 + offset_x, 240 + offset_y)
    Circle(canvas, x=200 + offset_x, y=219 + offset_y, r=20)


    canvas.create_text(250 + offset_x, 215 + offset_y, text="KUVAG NO VOLT", font=("Arial", 10), anchor="w")
    state.voltage_indicator = canvas.create_rectangle(370 + offset_x, 207 + offset_y, 390 + offset_x, 227 + offset_y, fill="green", outline="black")


    GroundSymbol(canvas, 130 + offset_x, 115 + offset_y)
    GroundSymbol(canvas, 130 + offset_x, 325 + offset_y)




    state.switch_parts = []
    switch = canvas.create_line(180 + offset_x, 80 + offset_y, 200 + offset_x, 105 + offset_y, width=2)
    state.switch_parts.append(switch)
    canvas.tag_bind(switch, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))
    hitbox1 = canvas.create_rectangle(170 + offset_x, 70 + offset_y, 210 + offset_x, 110 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox1, "<Button-1>", lambda e: switches.on_switch_click(e, canvas))


    state.lower_switch_parts = []
    lower = canvas.create_line(180 + offset_x, 340 + offset_y, 200 + offset_x, 315 + offset_y, width=2)
    state.lower_switch_parts.append(lower)
    canvas.tag_bind(lower, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))
    hitbox2 = canvas.create_rectangle(170 + offset_x, 305 + offset_y, 210 + offset_x, 345 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox2, "<Button-1>", lambda e: switches.on_lower_switch_click(e, canvas))


    state.middle_upper_parts = []
    upper_mid = canvas.create_line(180 + offset_x, 130 + offset_y, 200 + offset_x, 155 + offset_y, width=2)
    cross1 = canvas.create_line(195 + offset_x - 0, 130 + offset_y - 5, 195 + offset_x + 9, 130 + offset_y + 3, width=2)
    cross2 = canvas.create_line(195 + offset_x - 0, 130 + offset_y + 3, 195 + offset_x + 9, 130 + offset_y - 5, width=2)
    state.middle_upper_parts.append(upper_mid)
    canvas.tag_bind(upper_mid, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))
    hitbox3 = canvas.create_rectangle(170 + offset_x, 125 + offset_y, 210 + offset_x, 160 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox3, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))


    state.middle_lower_parts = []
    lower_mid = canvas.create_line(180 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y, width=2)
    cross1 = canvas.create_line(195 + offset_x - 0, 286 + offset_y - 7 + 2, 195 + offset_x + 9, 286 + offset_y + 1 + 2, width=2)
    cross2 = canvas.create_line(195 + offset_x - 0, 286 + offset_y + 1 + 2, 195 + offset_x + 9, 286 + offset_y - 7 + 2, width=2)
    state.middle_lower_parts.append(lower_mid)
    canvas.tag_bind(lower_mid, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))
    hitbox4 = canvas.create_rectangle(170 + offset_x, 255 + offset_y, 210 + offset_x, 290 + offset_y, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(hitbox4, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))


def draw_schematic_task2(canvas):
    offset_x = 0
    offset_y = 50
    spacing = 150
    shift_x = -75


    Line(canvas, 200 + offset_x + shift_x, 20 + offset_y, 200 + offset_x + spacing * 2 + shift_x, 20 + offset_y)


    second_busbar_start_x = 200 + spacing * 3 + shift_x
    second_busbar_y = 20 + offset_y
    Line(canvas, second_busbar_start_x, second_busbar_y, second_busbar_start_x + spacing * 2, second_busbar_y)


    draw_branch_frame(canvas, dx=offset_x + shift_x, dy=offset_y)
    custom_switches.register_three_switch(canvas, x=200 + offset_x + shift_x, y=105 + offset_y, group_id="cabinet1")
    custom_switches.register_two_switch(canvas, x=200 + offset_x + shift_x, y=155 + offset_y, group_id="cabinet1")


    draw_custom_branch_shaft_2(canvas, dx=offset_x + spacing + shift_x, dy=offset_y)



    draw_custom_branch_3_left(canvas, dx=spacing * 2 + shift_x, dy=offset_y)


    draw_custom_branch_3_right(canvas, dx=spacing * 2 + shift_x + 150, dy=offset_y)


    Line(canvas, 200 + spacing * 2 + shift_x, 180 + offset_y + 80,
         200 + spacing * 2 + shift_x + 150, 180 + offset_y + 80)


    draw_custom_branch_4(canvas, dx=spacing * 4 + shift_x, dy=offset_y)


    draw_custom_branch_5(canvas, dx=spacing * 5 + shift_x, dy=offset_y)

    # -------- BUS (левая шина) --------
def draw_synchro_lines(canvas):
    from logic import state

    # -------- BUS (левая шина) --------
    bus_horiz_1_start = (125, 70)
    bus_horiz_1_end   = (425, 70)

    bus_vert_x = 425
    bus_vert_top_y = 70
    bus_vert_bottom_y = 130

    # -------- LINE (правая шина) --------
    line_horiz_1_start = (875, 70)
    line_horiz_1_end   = (575, 70)

    line_vert_x = 575
    line_vert_top_y = 70
    line_vert_bottom_y = 130

    # -------- Нижняя перемычка --------
    bottom_y = 310
    bottom_left_x = bus_vert_x
    bottom_right_x = line_vert_x

    # -------- Внутрь BC --------
    center_top_y = 205
    center_bottom_y = 310

    # === Левая линия в BC
    bc_left_x1 = 425
    bc_left_y1 = 205
    bc_left_x2 = 425
    bc_left_y2 = 310

    # === Средняя линия в BC
    bc_middle_x1 = 425
    bc_middle_y1 = 155
    bc_middle_x2 = 425
    bc_middle_y2 = 180

    # === Правая линия в BC
    bc_right_x1 = 575
    bc_right_y1 = 155
    bc_right_x2 = 575
    bc_right_y2 = 310

    # === BUS
    state.synchro_bus_id = canvas.create_line(*bus_horiz_1_start, *bus_horiz_1_end, width=1, fill="black")
    state.synchro_bus_tail = canvas.create_line(bus_vert_x, bus_vert_top_y, bus_vert_x, bus_vert_bottom_y, width=1, fill="black")

    # === LINE
    state.synchro_line_id = canvas.create_line(*line_horiz_1_start, *line_horiz_1_end, width=1, fill="black")
    state.synchro_line_tail = canvas.create_line(line_vert_x, line_vert_top_y, line_vert_x, line_vert_bottom_y, width=1, fill="black")

    # === BC линии
    state.synchro_bridge = canvas.create_line(bottom_left_x, bottom_y, bottom_right_x, bottom_y, width=1, fill="black")
    state.synchro_bc_left = canvas.create_line(bc_left_x1, bc_left_y1, bc_left_x2, bc_left_y2, width=1, fill="black")
    state.synchro_bc_middle = canvas.create_line(bc_middle_x1, bc_middle_y1, bc_middle_x2, bc_middle_y2, width=1, fill="black")
    state.synchro_bc_right = canvas.create_line(bc_right_x1, bc_right_y1, bc_right_x2, bc_right_y2, width=1, fill="black")





def draw_custom_branch_shaft_2(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4




    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)


    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)


    Arrow(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension, direction="up")




    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet2")


    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet2")

def draw_custom_branch_3_left(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4


    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)


    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)


    Line(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension)


    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet3_left")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet3_left")

def draw_custom_branch_3_right(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4


    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)


    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Line(canvas, base_x, 105 + dy, base_x, 180 + dy + vertical_extension)


    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet3_right")

def draw_custom_branch_4(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4


    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)


    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)


    Arrow(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension, direction="up")


    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet4")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet4")

def draw_custom_branch_5(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70
    vertical_extension = 20 * 4


    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)


    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)
    Arrow(canvas, base_x, 155 + dy, base_x, 180 + dy + vertical_extension, direction="down")


    custom_switches.register_three_switch(canvas, x=base_x, y=105 + dy, group_id="cabinet5")
    custom_switches.register_two_switch(canvas, x=base_x, y=155 + dy, group_id="cabinet5")

def draw_branch_frame(canvas, dx, dy):
    base_x = 200 + dx
    ground_x = base_x - 70


    Line(canvas, base_x, 20 + dy, base_x, 80 + dy)

    Line(canvas, base_x, 105 + dy, base_x, 130 + dy)


    Line(canvas, base_x, 155 + dy, base_x, 155 + dy + 20 * 4)

    Line(canvas, ground_x, 105 + dy, base_x - 20, 105 + dy)


    GroundSymbol(canvas, ground_x, 115 + dy)


    Arrow(canvas, base_x, 180 + dy, base_x, 180 + dy + 20 * 4, direction="down")
