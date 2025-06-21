import customtkinter as ctk

def create_sidebar(parent):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text="Задачи", font=("Segoe UI", 16)).pack(pady=10)
    ctk.CTkButton(frame, text="Заглушка 1").pack(pady=5)
    ctk.CTkButton(frame, text="Заглушка 2").pack(pady=5)
    return frame
