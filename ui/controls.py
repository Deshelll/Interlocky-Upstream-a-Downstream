import tkinter as tk
from tkinter import ttk, Button, Label
from logic import switches
from logic.events import reset_trip, on_event_selected, manual_disable_middle_upper, manual_disable_middle_lower
from ui.style import themes

def setup_controls(root, canvas, alarm_text, alarm_rect):
    frame = tk.Frame(root, **themes.FRAME_STYLE)
    frame.pack(pady=10)

    toggle_button = tk.Button(frame, text="Změnit napětí", command=lambda: switches.toggle_voltage(canvas), **themes.BUTTON_STYLE)
    toggle_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    event_label = Label(frame, text="Vyber událost:", **themes.LABEL_STYLE)
    event_label.grid(row=5, column=0, padx=5, pady=(10, 0), sticky="w", columnspan=2)

    event_options = [
        "Žadné blokování", "Oil_temp_Alarm", "Oil_temp_Trip",
        "W_temp_Alarm", "W_temp_Trip", "Pressure_Relief",
        "Pressure_Alarm", "Pressure_Trip", "Level_Alarm",
        "Level_Trip", "Buchholz_Alarm", "Buchholz_Trip",
        "I0_Start (tank)", "I0_Trip (tank)", "Kvalita Silicagelu_Alarm"
    ]

    event_combobox = ttk.Combobox(frame, values=event_options, state="readonly", width=30)
    event_combobox.set("Vyber...")
    event_combobox.grid(row=6, column=0, padx=5, pady=(0, 10), sticky="w", columnspan=2)
    event_combobox.configure(font=themes.COMBOBOX_FONT)
    event_combobox.bind("<<ComboboxSelected>>", lambda e: on_event_selected(e, canvas, event_combobox, alarm_text, alarm_rect))

    label1 = Label(frame, text="Ručně vypnout vypínač Upstream", **themes.LABEL_STYLE)
    label1.grid(row=0, column=0, padx=5)
    button1 = Button(frame, text="Vypnout", command=lambda: manual_disable_middle_upper(canvas), **themes.BUTTON_STYLE)
    button1.grid(row=0, column=1, padx=5)

    label2 = Label(frame, text="Ručně vypnout vypínač Downstream", **themes.LABEL_STYLE)
    label2.grid(row=1, column=0, padx=5)
    button2 = Button(frame, text="Vypnout", command=lambda: manual_disable_middle_lower(canvas), **themes.BUTTON_STYLE)
    button2.grid(row=1, column=1, padx=5)

    reset_button = Button(frame, text="Reset Lockout", command=lambda: reset_trip(canvas, event_combobox, alarm_text, alarm_rect), **themes.BUTTON_STYLE)
    reset_button.grid(row=2, column=0, columnspan=2, pady=(5, 10))

    return event_combobox
