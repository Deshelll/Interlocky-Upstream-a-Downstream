from logic import state
from logic import switches

def reset_trip(canvas, event_combobox, alarm_text, alarm_rect):
    state.persistent_event = None
    event_combobox.set("Žadné blokování")
    canvas.itemconfig(alarm_text, text="")
    canvas.itemconfig(alarm_rect, fill="white")
    state.set_middle_upper_position_allowed = True
    state.set_middle_lower_position_allowed = True

def on_event_selected(event, canvas, event_combobox, alarm_text, alarm_rect):
    selected = event_combobox.get()
    persistent_trips = {
        "Pressure_Relief", "Oil_temp_Trip", "W_temp_Trip", "Pressure_Trip",
        "Level_Trip", "Buchholz_Alarm", "Buchholz_Trip", "I0_Trip (tank)"
    }

    if selected == "Žadné blokování" and state.persistent_event:
        canvas.itemconfig(alarm_text, text=state.persistent_event)
        canvas.itemconfig(alarm_rect, fill="red")
        return

    state.set_middle_upper_position_allowed = True
    state.set_middle_lower_position_allowed = True

    if selected in persistent_trips:
        state.persistent_event = selected
    else:
        state.persistent_event = None

    fill_color = "white"

    if selected == "Oil_temp_Alarm" or selected == "W_temp_Alarm":
        state.set_middle_lower_position_allowed = False

    elif selected == "Oil_temp_Trip" or selected == "W_temp_Trip":
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)
        state.set_middle_lower_position_allowed = False

    elif selected == "Pressure_Relief" or selected == "Buchholz_Alarm":
        if state.current_middle_upper_state == "on":
            switches.set_middle_upper_position("off", canvas)
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)
        state.set_middle_upper_position_allowed = False
        state.set_middle_lower_position_allowed = False

    elif selected == "Pressure_Alarm" or selected == "Level_Alarm":
        state.set_middle_upper_position_allowed = False
        state.set_middle_lower_position_allowed = False

    elif selected in ("Pressure_Trip", "Level_Trip", "Buchholz_Trip", "I0_Trip (tank)"):
        if state.current_middle_upper_state == "on":
            switches.set_middle_upper_position("off", canvas)
        if state.current_middle_lower_state == "on":
            switches.set_middle_lower_position("off", canvas)

    if selected != "Vyber..." and selected != "Žadné blokování":
        fill_color = "red"

    canvas.itemconfig(alarm_text, text=selected)
    canvas.itemconfig(alarm_rect, fill=fill_color)

def manual_disable_middle_upper(canvas):
    switches.set_middle_upper_position("off", canvas)

def manual_disable_middle_lower(canvas):
    switches.set_middle_lower_position("off", canvas)
