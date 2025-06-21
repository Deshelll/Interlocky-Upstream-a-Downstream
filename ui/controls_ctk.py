import customtkinter as ctk
from logic import switches
from logic.events import (
    reset_trip,
    on_event_selected,
    manual_disable_middle_upper,
    manual_disable_middle_lower,
)

def create_controls(parent, canvas, alarm_text, alarm_rect, event_combobox_ref):
    frame = ctk.CTkFrame(parent)

    ctk.CTkLabel(frame, text="Управление", font=("Segoe UI", 16)).pack(pady=10)

    ctk.CTkButton(frame, text="Změnit napětí", command=lambda: switches.toggle_voltage(canvas)).pack(pady=5)
    ctk.CTkButton(frame, text="Vypnout Upstream", command=lambda: manual_disable_middle_upper(canvas)).pack(pady=5)
    ctk.CTkButton(frame, text="Vypnout Downstream", command=lambda: manual_disable_middle_lower(canvas)).pack(pady=5)

    ctk.CTkLabel(frame, text="Vyber událost:").pack(pady=(15, 5))

    event_options = [
        "Žadné blokování", "Oil_temp_Alarm", "Oil_temp_Trip",
        "W_temp_Alarm", "W_temp_Trip", "Pressure_Relief",
        "Pressure_Alarm", "Pressure_Trip", "Level_Alarm",
        "Level_Trip", "Buchholz_Alarm", "Buchholz_Trip",
        "I0_Start (tank)", "I0_Trip (tank)", "Kvalita Silicagelu_Alarm"
    ]

    combobox = ctk.CTkComboBox(frame, values=event_options, width=280)
    combobox.set("Vyber...")
    combobox.pack(pady=5)

    # Связываем выбор события через .configure
    def handle_event_selection(choice):
        on_event_selected(None, canvas, combobox, alarm_text, alarm_rect)

    combobox.configure(command=handle_event_selection)

    # Передаём ссылку наружу
    event_combobox_ref[0] = combobox

    # Кнопка сброса тревоги
    ctk.CTkButton(
        frame,
        text="Reset Lockout",
        command=lambda: reset_trip(canvas, combobox, alarm_text, alarm_rect)
    ).pack(pady=(15, 10))

    return frame
