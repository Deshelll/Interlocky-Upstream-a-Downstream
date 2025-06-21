import tkinter as tk
from logic import state

def toggle_voltage(canvas):
    state.voltage_state = 1 - state.voltage_state
    color = "red" if state.voltage_state else "green"
    canvas.itemconfig(state.voltage_indicator, fill=color)

def mirror_point(x, y, horiz=True, vert=True):
    if horiz:
        x = state.X_center * 2 - x
    if vert:
        y = state.Y_center * 2 - y
    return x, y

def set_switch_position(position, canvas):
    if state.current_middle_upper_state == "on" and position in ("on", "short"):
        return
    if state.current_middle_upper_state == "on" and state.current_switch_state in ("on", "short") and position == "middle":
        return
    if state.voltage_state == 1 and position == "short":
        return
    if state.current_switch_state == "on" and position == "short":
        return

    for el in state.switch_parts:
        canvas.delete(el)
    state.switch_parts.clear()

    if position == "short":
        line = canvas.create_line(130, 105, 200, 105, width=2)
    elif position == "middle":
        line = canvas.create_line(180, 80, 200, 105, width=2)
    elif position == "on":
        line = canvas.create_line(200, 80, 200, 105, width=2)

    state.switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_switch_click(e, canvas))
    state.current_switch_state = position

def set_lower_switch_position(position, canvas):
    if state.current_middle_lower_state == "on" and position in ("on", "short"):
        return
    if state.current_middle_lower_state == "on" and state.current_lower_switch_state in ("on", "short") and position == "middle":
        return
    if state.current_lower_switch_state == "on" and position == "short":
        return
    if state.voltage_state == 1 and position == "short":
        return

    for el in state.lower_switch_parts:
        canvas.delete(el)
    state.lower_switch_parts.clear()

    if position == "short":
        line = canvas.create_line(130, 315, 200, 315, width=2)
    elif position == "middle":
        line = canvas.create_line(180, 340, 200, 315, width=2)
    elif position == "on":
        line = canvas.create_line(200, 340, 200, 315, width=2)

    state.lower_switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_lower_switch_click(e, canvas))
    state.current_lower_switch_state = position

def set_middle_upper_position(position, canvas):
    if not state.set_middle_upper_position_allowed and position == "on":
        return
    if (
        position == "on"
        and state.current_middle_lower_state == "on"
        and state.current_lower_switch_state == "on"
        and state.current_switch_state == "on"
    ):
        return
    if state.voltage_state == 1 and position == "on" and state.current_switch_state == "on":
        return
    if state.current_middle_upper_state == "on" and position == "off":
        set_middle_lower_position("off", canvas)
    if position == state.current_middle_upper_state:
        return

    for el in state.middle_upper_parts:
        canvas.delete(el)
    state.middle_upper_parts.clear()

    if position == "off":
        line = canvas.create_line(180, 130, 200, 155, width=2)
    elif position == "on":
        line = canvas.create_line(200, 130, 200, 155, width=2)

    state.middle_upper_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_upper_click(e, canvas))
    state.current_middle_upper_state = position

def set_middle_lower_position(position, canvas):
    if not state.set_middle_lower_position_allowed and position == "on":
        return
    if state.voltage_state == 1 and position == "on" and state.current_lower_switch_state == "on":
        return
    if position == state.current_middle_lower_state:
        return

    for el in state.middle_lower_parts:
        canvas.delete(el)
    state.middle_lower_parts.clear()

    if position == "off":
        line = canvas.create_line(180, 286, 200, 261, width=2)
    elif position == "on":
        line = canvas.create_line(200, 286, 200, 261, width=2)

    state.middle_lower_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_lower_click(e, canvas))
    state.current_middle_lower_state = position

def on_switch_click(event, canvas):
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="Zajet Disconneterem", command=lambda: set_switch_position("on", canvas))
    menu.add_command(label="Mezipoloha", command=lambda: set_switch_position("middle", canvas))
    menu.add_command(label="Zazkratovat", command=lambda: set_switch_position("short", canvas))
    menu.post(event.x + canvas.winfo_rootx(), event.y + canvas.winfo_rooty())

def on_lower_switch_click(event, canvas):
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="Zajet Disconneterem", command=lambda: set_lower_switch_position("on", canvas))
    menu.add_command(label="Mezipoloha", command=lambda: set_lower_switch_position("middle", canvas))
    menu.add_command(label="Zazkratovat", command=lambda: set_lower_switch_position("short", canvas))
    menu.post(event.x + canvas.winfo_rootx(), event.y + canvas.winfo_rooty())

def on_middle_upper_click(event, canvas):
    if state.current_switch_state == "short" and state.current_middle_upper_state == "on":
        return
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="Zapnout", command=lambda: set_middle_upper_position("on", canvas))
    menu.add_command(label="Vypnout", command=lambda: set_middle_upper_position("off", canvas))
    menu.post(event.x + canvas.winfo_rootx(), event.y + canvas.winfo_rooty())

def on_middle_lower_click(event, canvas):
    if state.current_lower_switch_state == "short" and state.current_middle_lower_state == "on":
        return
    menu = tk.Menu(canvas, tearoff=0)
    menu.add_command(label="Zapnout", command=lambda: set_middle_lower_position("on", canvas))
    menu.add_command(label="Vypnout", command=lambda: set_middle_lower_position("off", canvas))
    menu.post(event.x + canvas.winfo_rootx(), event.y + canvas.winfo_rooty())

def trip_transformer(canvas):
    if state.current_middle_upper_state == "on":
        set_middle_upper_position("off", canvas)
