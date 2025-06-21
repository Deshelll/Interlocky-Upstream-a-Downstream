import customtkinter as ctk

def create_sidebar(parent, show_task1_callback, show_task2_callback):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text="Задачи", font=("Segoe UI", 16)).pack(pady=10)
    ctk.CTkButton(frame, text="Задание 1", command=show_task1_callback).pack(pady=5)
    ctk.CTkButton(frame, text="Задание 2", command=show_task2_callback).pack(pady=5)
    return frame
