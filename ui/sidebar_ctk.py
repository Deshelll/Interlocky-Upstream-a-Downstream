import customtkinter as ctk

def create_sidebar(parent, show_task1_callback, show_task2_callback):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text="Schéma", font=("Segoe UI", 16)).pack(pady=10)
    ctk.CTkButton(frame, text="Up/Downstream", command=show_task1_callback).pack(pady=5)
    ctk.CTkButton(frame, text="2 INC, 2 OUT, BC", command=show_task2_callback).pack(pady=5)
    return frame
