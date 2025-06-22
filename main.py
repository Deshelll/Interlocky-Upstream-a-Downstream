import customtkinter as ctk
import tkinter as tk
from ui.sidebar_ctk import create_sidebar
from ui.controls_ctk import create_controls
from ui.controls_ctk import create_task2_controls
from ui.schematic import draw_schematic
from ui.schematic import draw_schematic_task2
from logic import state

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1200x700")
app.title("Interlocky Upstream a Downstream")

event_combobox_ref = [None]

canvas_frame = ctk.CTkFrame(app)
canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
canvas.pack(expand=True, fill="both")
state.canvas = canvas

controls_frame = None

def show_task1():
    global controls_frame
    app.geometry("1200x700")
    canvas_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    canvas.delete("all")
    draw_schematic(canvas)

    alarm_rect = canvas.create_rectangle(10, 420, 30, 440, fill="white", outline="black")
    alarm_text = canvas.create_text(35, 430, text="", anchor="w", font=("Arial", 10), fill="black")

    if controls_frame:
        controls_frame.pack_forget()
    controls_frame_new = create_controls(app, canvas, alarm_text, alarm_rect, event_combobox_ref)
    controls_frame_new.pack(side="right", fill="y", padx=10, pady=10)
    controls_frame = controls_frame_new

def show_task2():
    global controls_frame
    app.geometry("1350x700")
    canvas_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    canvas.delete("all")
    draw_schematic_task2(canvas)

    if controls_frame:
        controls_frame.pack_forget()
    controls_frame = create_task2_controls(app, canvas)
    controls_frame.pack(side="right", fill="y", padx=10, pady=10)

sidebar = create_sidebar(app, show_task1, show_task2)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

app.mainloop()
