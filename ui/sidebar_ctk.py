import customtkinter as ctk
from ui.translations import t, switch_language, get_current_language


def create_sidebar(parent, show_task1_callback, show_task2_callback, show_home_callback, restart_callback):
    frame = ctk.CTkFrame(parent)

    # Верхние кнопки
    ctk.CTkButton(frame, text=t("home"), font=("Segoe UI", 16), command=show_home_callback).pack(pady=10)
    ctk.CTkButton(frame, text=t("task1"), command=show_task1_callback).pack(pady=5)
    ctk.CTkButton(frame, text=t("task2"), command=show_task2_callback).pack(pady=5)

    language_options = {
        "cs": "Čeština",
        "en": "English",
        "ru": "Russian"
    }

    def on_language_selected(label):
        for code, name in language_options.items():
            if name == label:
                switch_language(code)
                restart_callback()
                break

    current_label = language_options.get(get_current_language(), "Language")

    language_selector = ctk.CTkOptionMenu(
        frame,
        values=list(language_options.values()),
        command=on_language_selected,
        width=100,
        height=28,
        anchor="center"
    )

    language_selector.set(current_label)
    language_selector.pack(side="bottom", pady=10)
    return frame
