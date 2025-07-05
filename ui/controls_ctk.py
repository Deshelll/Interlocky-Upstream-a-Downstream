import customtkinter as ctk
from logic import switches
from logic import state
import customtkinter as ctk
from logic import custom_switches
from ui.schematic import draw_synchro_lines
from logic.events import (
    reset_trip,
    on_event_selected,
    manual_disable_middle_upper,
    manual_disable_middle_lower,
)
from canvas_elements import synchrocheck
from ui.translations import t, switch_language

def create_controls(parent, canvas, alarm_text, alarm_rect, event_combobox_ref):
    frame = ctk.CTkFrame(parent)
    
    def on_language_toggle():
        switch_language()
        # ❗ Тут нужно перерисовать весь интерфейс или пересоздать frame
        frame.destroy()
        new_frame = create_controls(parent, canvas, alarm_text, alarm_rect, event_combobox_ref)
        new_frame.pack()  # заново отрисовать

    ctk.CTkLabel(frame, text=t("Manipulate"), font=("Segoe UI", 16)).pack(pady=10)

    ctk.CTkButton(frame, text=t("toggle_voltage"), command=lambda: switches.toggle_voltage(canvas)).pack(pady=5)
    ctk.CTkButton(frame, text=t("disable_upstream"), command=lambda: manual_disable_middle_upper(canvas)).pack(pady=5)
    ctk.CTkButton(frame, text=t("disable_downstream"), command=lambda: manual_disable_middle_lower(canvas)).pack(pady=5)
    
    ctk.CTkLabel(frame, text=t("select_event")).pack(pady=(15, 5))

    event_keys = [
        "event_none", "oil_temp_alarm", "oil_temp_trip",
        "w_temp_alarm", "w_temp_trip", "pressure_relief",
        "pressure_alarm", "pressure_trip", "level_alarm",
        "level_trip", "buchholz_alarm", "buchholz_trip",
        "i0_start", "i0_trip", "silicagel_alarm"
    ]

    event_options = [t(key) for key in event_keys]
    event_key_map = {t(key): key for key in event_keys}
    state.event_key_map = event_key_map
    combobox = ctk.CTkComboBox(frame, values=event_options, width=280)
    combobox.set(t("choose"))
    combobox.pack(pady=5)


    def handle_event_selection(choice):
        selected_label = combobox.get()
        selected_key = state.event_key_map.get(selected_label, None)
        on_event_selected(None, canvas, combobox, alarm_text, alarm_rect)

    combobox.configure(command=handle_event_selection)


    event_combobox_ref[0] = combobox


    ctk.CTkButton(
        frame,
        text=t("reset"),
        command=lambda: reset_trip(canvas, combobox, alarm_text, alarm_rect)
    ).pack(pady=(15, 10))

    return frame
    
    
def create_task2_controls(parent, canvas, synchro_ui):
    from canvas_elements import synchrocheck 
    from canvas_elements.synchrocheck_ui import SynchroUI
    state.synchro_ui = synchro_ui
    frame = ctk.CTkFrame(parent, width=200)
    frame.pack_propagate(False)
    frame.pack(fill="y", padx=10, pady=10)
    synchro = synchrocheck(canvas)
    ctk.CTkLabel(frame, text=t("task2_title"), font=("Segoe UI", 14)).pack(pady=(10, 10))

    buttons = [
        (t("disable_out_1"), "cabinet1"),
        (t("disable_inc_1"), "cabinet2"),
        (t("disable_bc"), "cabinet3_left"),
        (t("disable_inc_2"), "cabinet4"),
        (t("disable_out_2"), "cabinet5"),
    ]
    for label, group_id in buttons:
        ctk.CTkButton(frame, text=label, width=180, height=28,
                      command=lambda g=group_id: custom_switches.force_turn_off_two_switches_by_group(g))\
            .pack(pady=5, padx=10)



    
    synchro_ui.mode_dropdown.pack_forget()
    synchro_ui.mode_dropdown.pack(pady=10)

    def toggle_all():
        synchro.toggle()
        synchro_ui.toggle()


        if synchro_ui.visible:
            synchro_ui.mode_dropdown.pack(pady=10)
            draw_synchro_lines(canvas)
            synchro_ui.update_line_colors()
        else:
            synchro_ui.mode_dropdown.pack_forget()


    ctk.CTkButton(frame, text=t("synchrocheck"), command=toggle_all).pack(pady=5)
    return frame
