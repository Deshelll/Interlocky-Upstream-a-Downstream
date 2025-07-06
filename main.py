import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from ui.sidebar_ctk import create_sidebar
from ui.controls_ctk import create_controls
from ui.controls_ctk import create_task2_controls
from ui.schematic import draw_schematic, draw_schematic_task2
from logic import state
from logic import custom_switches
from canvas_elements import synchrocheck_ui
from canvas_elements.synchrocheck_ui import SynchroUI
from ui.translations import load_language_choice
from logic.custom_switches import draw_cross
import sys, os

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, работает и в .py, и в .exe"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_ui(app):
    global canvas, sidebar, controls_frame, event_combobox_ref
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app.iconbitmap(default=resource_path("assets/bba.ico"))
    app.geometry("1200x700")
    app.title("Interlocky")

    event_combobox_ref = [None]


    canvas_frame = ctk.CTkFrame(app)
    canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    state.canvas = canvas

    logo_bind_id = None

    try:
        logo_image = Image.open(resource_path("assets/logo.png"))
        logo_image = logo_image.resize((805, 453), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_image)
        canvas.logo = logo_tk

        def place_logo_center(event=None):
            canvas.delete("logo")
            x = canvas.winfo_width() // 2
            y = canvas.winfo_height() // 2
            canvas.create_image(x, y, image=canvas.logo, anchor="center", tags="logo")

        logo_bind_id = canvas.bind("<Configure>", place_logo_center)

    except Exception as e:
        print("[LOGO ERROR]", e)

    controls_frame = None

    def show_home():
        global controls_frame
        app.geometry("1200x700")
        reset_all_ui_states(canvas)
        canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=canvas.logo, anchor="center", tags="logo")
        canvas.bind("<Configure>", place_logo_center)

        if controls_frame:
            controls_frame.pack_forget()
            controls_frame = None

    def show_task1():
        global controls_frame
        app.geometry("1200x700")
        reset_all_ui_states(canvas)

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
        reset_all_ui_states(canvas)
        draw_schematic_task2(canvas)

        if controls_frame:
            controls_frame.pack_forget()
        controls_frame = create_task2_controls(app, canvas, state.synchro_ui)
        controls_frame.pack(side="right", fill="y", padx=10, pady=10)
        
    def reset_all_ui_states(canvas):
        import logic.custom_switches as custom_switches
        import logic.state as state

        canvas.unbind("<Configure>")
        canvas.delete("all")

        # Сброс логических флагов
        state.persistent_event = None
        state.voltage_state = 0
        state.voltage_indicator = None
        state.set_middle_upper_position_allowed = True
        state.set_middle_lower_position_allowed = True

        # Сброс переключателей
        state.current_switch_state = "middle"
        state.current_lower_switch_state = "middle"
        state.current_middle_upper_state = "off"
        state.current_middle_lower_state = "off"

        # Очистка схемы
        custom_switches.custom_switches.clear()
        state.switch_parts.clear()
        state.lower_switch_parts.clear()
        state.middle_upper_parts.clear()
        state.middle_lower_parts.clear()

        # Скрыть SynchroUI и логику
        if hasattr(state, "synchro_ui") and state.synchro_ui.visible:
            state.synchro_ui.toggle()
        if hasattr(state, "synchrocheck_logic") and state.synchrocheck_logic.active:
            state.synchrocheck_logic.deactivate()


    sidebar = create_sidebar(app, show_task1, show_task2, show_home, restart_app)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)


    canvas_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    state.synchro_ui = SynchroUI(canvas_frame)


def start_app():
    global app
    app = ctk.CTk()
    app.iconbitmap(default=resource_path("assets/bba.ico"))
    app.geometry("1200x700")
    app.title("Interlocky")

    run_ui(app)  # просто запусти UI
    app.mainloop()

def restart_app():
    for widget in app.winfo_children():
        widget.destroy()
    run_ui(app)  # перезапуск всей UI-логики в том же окне



if __name__ == "__main__":
    load_language_choice()
    start_app()


