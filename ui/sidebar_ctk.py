import customtkinter as ctk

def create_sidebar(parent, show_task1_callback, show_task2_callback, show_home_callback):
    frame = ctk.CTkFrame(parent)
    ctk.CTkButton(frame, text="Home", font=("Segoe UI", 16), command=show_home_callback).pack(pady=10)
    ctk.CTkButton(frame, text="Up/Downstream", command=show_task1_callback).pack(pady=5)
    ctk.CTkButton(frame, text="2 INC, 2 OUT, BC", command=show_task2_callback).pack(pady=5)
    return frame
