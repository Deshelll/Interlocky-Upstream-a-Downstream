import tkinter as tk
import customtkinter as ctk
from logic import state
from ui.context_menu import CustomContextMenu
from canvas_elements import Line, GroundSymbol
from logic import state, switches



def is_switch_transition_allowed(position):

    if position == "short" and state.current_lower_switch_state == "on":
        return ("lower_on_block", "Nelze zazkratovat, pokud je disconnector Downstream připojen k přípojnici")


    if position == "on" and state.current_lower_switch_state == "short":
        return ("lower_short_block", "Nelze zapnout: Downstream zkratovač je zkratován")
    if state.current_switch_state == position:
        return "current"
    if state.current_middle_upper_state == "on" and position in ("on", "short"):
        return ("middle_upper", "Nelze vybrat: Upstream vypínač je již zapnutý")
    if state.current_middle_upper_state == "on" and state.current_switch_state in ("on", "short") and position == "middle":
        return ("mid_back", "Nejdříve musíte vypnout vypínač")
    if state.voltage_state == 1 and position == "short":
        return ("voltage_short", "Nelze zazkratovat, pokud je na kabelech napětí")
    if state.current_switch_state == "on" and position == "short":
        return ("on_short", "Nelze přeskočit mezipolohu mezi „Disconnector On“ a „Zazkratovat“")
    return True

def is_lower_switch_transition_allowed(position):

    if position == "short" and state.current_switch_state == "on":
        return ("upper_on_block", "Nelze zazkratovat, pokud je disconnector Upstream připojen k přípojnici")


    if position == "on" and state.current_switch_state == "short":
        return ("upper_short_block", "Nelze zapnout: Upstream zkratovač je zkratován")
    if state.current_lower_switch_state == position:
        return "current"
    if not state.set_middle_lower_position_allowed and position == "on":
        return ("not_allowed", "Zapnutí je zakázáno")
    if position in ("on", "short") and state.current_lower_switch_state != "middle":
        return ("not_middle", "Nelze přeskočit mezipolohu mezi „Disconnector On“ a „Zazkratovat“")
    if state.current_middle_lower_state == "on" and position in ("on", "short"):
        return ("ml_on", "Downstream vypínač je v poloze „zapnuto“")
    if state.current_middle_lower_state == "on" and state.current_lower_switch_state in ("on", "short") and position == "middle":
        return ("ml_mid_block", "Nelze přepnout do mezipolohy — vypínač je aktivní.")
    if state.current_lower_switch_state == "on" and position == "short":
        return ("lower_on_short", "Nejdříve musíte vypnout vypínač")
    if state.voltage_state == 1 and position == "short":
        return ("voltage_short", "Nelze zazkratovat, pokud je na kabelech napětí")
    return True

def is_middle_upper_transition_allowed(position):

    if position == "off":
        if state.current_switch_state == "short":
            return ("short_block", "Odzkratujte pomocí manuálního tlačítka")
    if state.current_middle_upper_state == position:
        return "current"
    if not state.set_middle_upper_position_allowed and position == "on":
        return ("not_allowed", "Resetujte Lockout")
    if (
        position == "on"
        and state.current_middle_lower_state == "on"
        and state.current_lower_switch_state == "on"
        and state.current_switch_state == "on"
    ):
        return ("all_on", "Všechny vypínače jsou zapnuté")
    return True

def is_middle_lower_transition_allowed(position):

    if position == "off" and state.current_middle_lower_state == "on":
        if state.current_lower_switch_state == "short":
            return ("short_block", "Pro odzkratování použijte manuální tlačítko")


    if state.current_middle_lower_state == position:
        return "current"

    if not state.set_middle_lower_position_allowed and position == "on":
        return ("not_allowed", "Resetujte Lockout")
    if position == "on" and state.current_middle_upper_state != "on":
        return ("mu_off", "Nejdříve musíte zapnout vypínač Upstream")
    if state.voltage_state == 1 and position == "on" and state.current_lower_switch_state == "on":
        return ("voltage_block", "Na kabelech je napětí")

    return True



def toggle_voltage(canvas):
    state.voltage_state = 1 - state.voltage_state
    color = "red" if state.voltage_state else "green"
    canvas.itemconfig(state.voltage_indicator, fill=color)

def set_switch_position(position, canvas):
    offset_x = 150
    offset_y = 50

    if not is_switch_transition_allowed(position) == True:
        return
    for el in state.switch_parts:
        canvas.delete(el)
    state.switch_parts.clear()
    coords = {
        "short": (130 + offset_x, 105 + offset_y, 200 + offset_x, 105 + offset_y),
        "middle": (180 + offset_x, 80 + offset_y, 200 + offset_x, 105 + offset_y),
        "on": (200 + offset_x, 80 + offset_y, 200 + offset_x, 105 + offset_y)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_switch_click(e, canvas))
    state.current_switch_state = position

def set_lower_switch_position(position, canvas):
    offset_x = 150
    offset_y = 50

    if not is_lower_switch_transition_allowed(position) == True:
        return
    for el in state.lower_switch_parts:
        canvas.delete(el)
    state.lower_switch_parts.clear()
    coords = {
        "short": (130 + offset_x, 315 + offset_y, 200 + offset_x, 315 + offset_y),
        "middle": (180 + offset_x, 340 + offset_y, 200 + offset_x, 315 + offset_y),
        "on": (200 + offset_x, 340 + offset_y, 200 + offset_x, 315 + offset_y)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.lower_switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_lower_switch_click(e, canvas))
    state.current_lower_switch_state = position

def set_middle_upper_position(position, canvas):
    offset_x = 150
    offset_y = 50

    if not is_middle_upper_transition_allowed(position) == True:
        return

    for el in state.middle_upper_parts:
        canvas.delete(el)
    state.middle_upper_parts.clear()

    coords = {
        "off": (180 + offset_x, 130 + offset_y, 200 + offset_x, 155 + offset_y),
        "on": (200 + offset_x, 130 + offset_y, 200 + offset_x, 155 + offset_y)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.middle_upper_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_upper_click(e, canvas))
    state.current_middle_upper_state = position

    if position == "off":

        state.current_middle_lower_state = "off"
        for el in state.middle_lower_parts:
            canvas.delete(el)
        state.middle_lower_parts.clear()
        lower_coords = (180 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y)
        lower_line = canvas.create_line(*lower_coords, width=2)
        state.middle_lower_parts.append(lower_line)
        canvas.tag_bind(lower_line, "<Button-1>", lambda e: on_middle_lower_click(e, canvas))


def set_middle_lower_position(position, canvas):
    offset_x = 150
    offset_y = 50

    if not is_middle_lower_transition_allowed(position) == True:
        return
    for el in state.middle_lower_parts:
        canvas.delete(el)
    state.middle_lower_parts.clear()
    coords = {
        "off": (180 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y),
        "on": (200 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.middle_lower_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_lower_click(e, canvas))
    state.current_middle_lower_state = position



def on_switch_click(event, canvas):
    menu = CustomContextMenu(canvas)
    items = [("on", "Zajet Disconnectorem"), ("middle", "Mezipoloha"), ("short", "Zazkratovat")]

    allowed_map = {pos: is_switch_transition_allowed(pos) for pos, _ in items}
    any_enabled = any(v is True for v in allowed_map.values())

    for pos, label in items:
        result = allowed_map[pos]
        highlight = (result == "current") if any_enabled else False
        tooltip = None
        if isinstance(result, tuple):
            tooltip = result[1]
        elif highlight:
            tooltip = "Jste již v této poloze"
        menu.add_option(label, lambda p=pos: set_switch_position(p, canvas), enabled=(result is True), highlight=highlight, tooltip_text=tooltip)

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()

def on_lower_switch_click(event, canvas):
    menu = CustomContextMenu(canvas)
    items = [("on", "Zajet Disconnectorem"), ("middle", "Mezipoloha"), ("short", "Zazkratovat")]

    allowed_map = {pos: is_lower_switch_transition_allowed(pos) for pos, _ in items}
    any_enabled = any(v is True for v in allowed_map.values())

    for pos, label in items:
        result = allowed_map[pos]
        highlight = (result == "current") if any_enabled else False
        tooltip = None
        if isinstance(result, tuple):
            tooltip = result[1]
        elif highlight:
            tooltip = "Jste již v této poloze"
        menu.add_option(label, lambda p=pos: set_lower_switch_position(p, canvas), enabled=(result is True), highlight=highlight, tooltip_text=tooltip)

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()

def on_middle_upper_click(event, canvas):
    menu = CustomContextMenu(canvas)
    items = [("on", "Zapnout"), ("off", "Vypnout")]

    allowed_map = {pos: is_middle_upper_transition_allowed(pos) for pos, _ in items}
    any_enabled = any(v is True for v in allowed_map.values())

    for pos, label in items:
        result = allowed_map[pos]
        highlight = (result == "current") if any_enabled else False
        tooltip = None
        if isinstance(result, tuple):
            tooltip = result[1]
        elif highlight:
            tooltip = "Jste již v této poloze"
        menu.add_option(label, lambda p=pos: set_middle_upper_position(p, canvas), enabled=(result is True), highlight=highlight, tooltip_text=tooltip)

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()

def on_middle_lower_click(event, canvas):
    menu = CustomContextMenu(canvas)
    items = [("on", "Zapnout"), ("off", "Vypnout")]

    allowed_map = {pos: is_middle_lower_transition_allowed(pos) for pos, _ in items}
    any_enabled = any(v is True for v in allowed_map.values())

    for pos, label in items:
        result = allowed_map[pos]
        highlight = (result == "current") if any_enabled else False
        tooltip = None
        if isinstance(result, tuple):
            tooltip = result[1]
        elif highlight:
            tooltip = "Jste již v této poloze"
        menu.add_option(label, lambda p=pos: set_middle_lower_position(p, canvas), enabled=(result is True), highlight=highlight, tooltip_text=tooltip)

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()

def trip_transformer(canvas):
    if state.current_middle_upper_state == "on":
        set_middle_upper_position("off", canvas)
