import tkinter as tk
import customtkinter as ctk
from logic import state
from ui.context_menu import CustomContextMenu

# ====== Проверки допустимости переходов ======

def is_switch_transition_allowed(position):
    if state.current_switch_state == position:
        return "current"
    if state.current_middle_upper_state == "on" and position in ("on", "short"):
        return ("middle_upper", "Нельзя выбрать: верхний средний ключ уже включён")
    if state.current_middle_upper_state == "on" and state.current_switch_state in ("on", "short") and position == "middle":
        return ("mid_back", "Сначала нужно перевести выключатель в положение 'выкл.'")
    if state.voltage_state == 1 and position == "short":
        return ("voltage_short", "Нельзя замкнуть при поданном напряжении")
    if state.current_switch_state == "on" and position == "short":
        return ("on_short", "Нельзя сразу перейти из 'вкл.' в замыкание")
    return True

def is_lower_switch_transition_allowed(position):
    if state.current_lower_switch_state == position:
        return "current"
    if not state.set_middle_lower_position_allowed and position == "on":
        return ("not_allowed", "Переход во 'вкл.' запрещён политикой")
    if position in ("on", "short") and state.current_lower_switch_state != "middle":
        return ("not_middle", "Можно переключиться только из 'среднего' положения")
    if state.current_middle_lower_state == "on" and position in ("on", "short"):
        return ("ml_on", "Средний нижний ключ уже во 'вкл.'")
    if state.current_middle_lower_state == "on" and state.current_lower_switch_state in ("on", "short") and position == "middle":
        return ("ml_mid_block", "Нельзя вернуться в 'среднее' — активна средняя линия")
    if state.current_lower_switch_state == "on" and position == "short":
        return ("lower_on_short", "Нельзя замкнуть при активном нижнем ключе")
    if state.voltage_state == 1 and position == "short":
        return ("voltage_short", "Нельзя замкнуть при поданном напряжении")
    return True

def is_middle_upper_transition_allowed(position):
    if state.current_middle_upper_state == position:
        return "current"
    if not state.set_middle_upper_position_allowed and position == "on":
        return ("not_allowed", "Переход во 'вкл.' запрещён политикой")
    if (
        position == "on"
        and state.current_middle_lower_state == "on"
        and state.current_lower_switch_state == "on"
        and state.current_switch_state == "on"
    ):
        return ("all_on", "Нельзя включить: все ключи уже активны")
    if state.voltage_state == 1 and position == "on" and state.current_switch_state == "on":
        return ("voltage_block", "Подано напряжение при активном ключе")
    return True

def is_middle_lower_transition_allowed(position):
    if state.current_middle_lower_state == position:
        return "current"
    if not state.set_middle_lower_position_allowed and position == "on":
        return ("not_allowed", "Переход во 'вкл.' запрещён политикой")
    if position == "on" and state.current_middle_upper_state != "on":
        return ("mu_off", "Нельзя включить: верхний средний ключ не во 'вкл.'")
    if state.voltage_state == 1 and position == "on" and state.current_lower_switch_state == "on":
        return ("voltage_block", "Подано напряжение при активном нижнем ключе")
    return True

# ====== Смена состояния ======

def toggle_voltage(canvas):
    state.voltage_state = 1 - state.voltage_state
    color = "red" if state.voltage_state else "green"
    canvas.itemconfig(state.voltage_indicator, fill=color)

def set_switch_position(position, canvas):
    if not is_switch_transition_allowed(position) == True:
        return
    for el in state.switch_parts:
        canvas.delete(el)
    state.switch_parts.clear()
    coords = {
        "short": (130, 105, 200, 105),
        "middle": (180, 80, 200, 105),
        "on": (200, 80, 200, 105)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_switch_click(e, canvas))
    state.current_switch_state = position

def set_lower_switch_position(position, canvas):
    if not is_lower_switch_transition_allowed(position) == True:
        return
    for el in state.lower_switch_parts:
        canvas.delete(el)
    state.lower_switch_parts.clear()
    coords = {
        "short": (130, 315, 200, 315),
        "middle": (180, 340, 200, 315),
        "on": (200, 340, 200, 315)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.lower_switch_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_lower_switch_click(e, canvas))
    state.current_lower_switch_state = position

def set_middle_upper_position(position, canvas):
    if not is_middle_upper_transition_allowed(position) == True:
        return
    for el in state.middle_upper_parts:
        canvas.delete(el)
    state.middle_upper_parts.clear()
    coords = {
        "off": (180, 130, 200, 155),
        "on": (200, 130, 200, 155)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.middle_upper_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_upper_click(e, canvas))
    state.current_middle_upper_state = position
    if position == "off":
        set_middle_lower_position("off", canvas)

def set_middle_lower_position(position, canvas):
    if not is_middle_lower_transition_allowed(position) == True:
        return
    for el in state.middle_lower_parts:
        canvas.delete(el)
    state.middle_lower_parts.clear()
    coords = {
        "off": (180, 286, 200, 261),
        "on": (200, 286, 200, 261)
    }
    line = canvas.create_line(*coords[position], width=2)
    state.middle_lower_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: on_middle_lower_click(e, canvas))
    state.current_middle_lower_state = position

# ====== Контекстные меню ======

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
            tooltip = "Нельзя выбрать этот пункт, т.к. вы уже находитесь в нём"
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
            tooltip = "Нельзя выбрать этот пункт, т.к. вы уже находитесь в нём"
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
            tooltip = "Нельзя выбрать этот пункт, т.к. вы уже находитесь в нём"
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
            tooltip = "Нельзя выбрать этот пункт, т.к. вы уже находитесь в нём"
        menu.add_option(label, lambda p=pos: set_middle_lower_position(p, canvas), enabled=(result is True), highlight=highlight, tooltip_text=tooltip)

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()

def trip_transformer(canvas):
    if state.current_middle_upper_state == "on":
        set_middle_upper_position("off", canvas)
