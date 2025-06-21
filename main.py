import customtkinter as ctk
import tkinter as tk
from ui.sidebar_ctk import create_sidebar
from ui.controls_ctk import create_controls
from ui.schematic import draw_schematic
from logic import state

# Настройки интерфейса
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Главное окно
app = ctk.CTk()
app.geometry("1200x700")
app.title("Interlocky Upstream a Downstream")

# === Левая панель (выбор задачи) ===
sidebar = create_sidebar(app)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

# === Центральная панель (canvas) ===
canvas_frame = ctk.CTkFrame(app)
canvas_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
canvas.pack(expand=True, fill="both")
state.canvas = canvas  # если нужно где-то использовать

# === Элементы тревоги (видны на схеме) ===
alarm_rect = canvas.create_rectangle(10, 420, 30, 440, fill="white", outline="black")
alarm_text = canvas.create_text(35, 430, text="", anchor="w", font=("Arial", 10), fill="black")

# === Комбо-бокс с событиями — создаётся в controls и передаётся через ссылку ===
event_combobox_ref = [None]

# === Правая панель управления ===
controls = create_controls(app, canvas, alarm_text, alarm_rect, event_combobox_ref)
controls.pack(side="right", fill="y", padx=10, pady=10)

# === Отрисовка схемы ===
draw_schematic(canvas)

# Запуск GUI
app.mainloop()
