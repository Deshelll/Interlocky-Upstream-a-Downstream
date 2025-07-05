from logic import state
from logic import switches
from ui.translations import t

# Ключи событий
event_keys = [
    "event_none", "oil_temp_alarm", "oil_temp_trip",
    "w_temp_alarm", "w_temp_trip",
    "pressure_relief", "pressure_alarm", "pressure_trip",
    "level_alarm", "level_trip",
    "buchholz_alarm", "buchholz_trip",
    "i0_start", "i0_trip", "silicagel_alarm"
]

# Ключи, считающиеся "постоянными авариями"
persistent_trips = {
    "pressure_relief", "oil_temp_trip", "w_temp_trip", "pressure_trip",
    "level_trip", "buchholz_alarm", "buchholz_trip", "i0_trip"
}

# Мапа: отображаемый текст → ключ
def get_event_key_map():
    return {t(key): key for key in event_keys}


def reset_trip(canvas, event_combobox, alarm_text, alarm_rect):
    state.persistent_event = None
    event_combobox.set(t("event_none"))
    canvas.itemconfig(alarm_text, text="")
    canvas.itemconfig(alarm_rect, fill="white")
    state.set_middle_upper_position_allowed = True
    state.set_middle_lower_position_allowed = True


def on_event_selected(event, canvas, event_combobox, alarm_text, alarm_rect):
    selected_label = event_combobox.get()
    selected_key = get_event_key_map().get(selected_label, None)

    if selected_key == "event_none" and state.persistent_event:
        canvas.itemconfig(alarm_text, text=state.persistent_event)
        canvas.itemconfig(alarm_rect, fill="red")
        return

    state.set_middle_upper_position_allowed = True
    state.set_middle_lower_position_allowed = True

    if selected_key in persistent_trips:
        state.persistent_event = t(selected_key)
    else:
        state.persistent_event = None

    fill_color = "white"

    # Логика отключений
    if selected_key == "oil_temp_alarm" or selected_key == "w_temp_alarm":
        state.set_middle_lower_position_allowed = False

    elif selected_key == "oil_temp_trip" or selected_key == "w_temp_trip":
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)
        state.set_middle_lower_position_allowed = False

    elif selected_key == "pressure_relief" or selected_key == "buchholz_alarm":
        if state.current_middle_upper_state == "on":
            switches.set_middle_upper_position("off", canvas)
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)
        state.set_middle_upper_position_allowed = False
        state.set_middle_lower_position_allowed = False

    elif selected_key == "pressure_alarm" or selected_key == "level_alarm":
        state.set_middle_upper_position_allowed = False
        state.set_middle_lower_position_allowed = False

    elif selected_key in ("pressure_trip", "level_trip", "buchholz_trip", "i0_trip"):
        if state.current_middle_upper_state == "on":
            switches.set_middle_upper_position("off", canvas)
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)

    if selected_key not in (None, "event_none"):
        fill_color = "red"

    canvas.itemconfig(alarm_text, text=t(selected_key) if selected_key else "")
    canvas.itemconfig(alarm_rect, fill=fill_color)


def manual_disable_middle_upper(canvas):
    state.current_middle_upper_state = "off"
    for el in state.middle_upper_parts:
        canvas.delete(el)
    state.middle_upper_parts.clear()

    offset_x = 150
    offset_y = 50
    coords = (180 + offset_x, 130 + offset_y, 200 + offset_x, 155 + offset_y)
    line = canvas.create_line(*coords, width=2)
    state.middle_upper_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: switches.on_middle_upper_click(e, canvas))

    manual_disable_middle_lower(canvas)


def manual_disable_middle_lower(canvas):
    state.current_middle_lower_state = "off"
    for el in state.middle_lower_parts:
        canvas.delete(el)
    state.middle_lower_parts.clear()

    offset_x = 150
    offset_y = 50
    coords = (180 + offset_x, 286 + offset_y, 200 + offset_x, 261 + offset_y)
    line = canvas.create_line(*coords, width=2)
    state.middle_lower_parts.append(line)
    canvas.tag_bind(line, "<Button-1>", lambda e: switches.on_middle_lower_click(e, canvas))
