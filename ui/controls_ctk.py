import customtkinter as ctk
from logic import switches
import customtkinter as ctk
from logic import custom_switches
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
    
    
def create_task2_controls(parent, canvas):

    frame = ctk.CTkFrame(parent, width=200)  # ширина такая же, как у task1
    frame.pack_propagate(False)  # чтобы не сжимался
    frame.pack(fill="y", padx=10, pady=10)

    ctk.CTkLabel(frame, text="Ruční vypnutí", font=("Segoe UI", 14)).pack(pady=(10, 10))

    buttons = [
        ("Vypnout vypínač OUT 1", "cabinet1"),
        ("Vypnout vypínač INC", "cabinet2"),
        ("Vypnout vypínač BC", "cabinet3"),
        ("Vypnout vypínač INC 2", "cabinet4"),
        ("Vypnout vypínač OUT 2", "cabinet5"),
    ]

    for label, group_id in buttons:
        ctk.CTkButton(frame, text=label, width=180, height=28,
                      command=lambda g=group_id: custom_switches.force_turn_off_two_switches_by_group(g))\
            .pack(pady=5, padx=10)

    return frame