import customtkinter as ctk
from ui.exclamation_icon import ExclamationIcon

class CustomContextMenu:
    def __init__(self, master):
        self.window = ctk.CTkToplevel(master)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(fg_color="#1a1a1a")  # Цвет фона окна
        #self.window.bind("<FocusOut>", lambda e: self.window.destroy())
        self.window.grab_set()

    def add_option(self, label, command, enabled=True, highlight=False, tooltip_text=None):
        frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        frame.pack(fill="x", padx=8, pady=2)

        if enabled:
            btn = ctk.CTkLabel(frame, text=label, width=120, anchor="w", cursor="hand2")
            btn.bind("<Enter>", lambda e: btn.configure(fg_color="#333333"))
            btn.bind("<Leave>", lambda e: btn.configure(fg_color="#1a1a1a"))
            btn.bind("<Button-1>", lambda e: (command(), self.window.destroy()))
        else:
            btn = ctk.CTkLabel(
                frame, text=label, width=120, anchor="w",
                fg_color="#1a1a1a", text_color="gray"
            )

        btn.pack(side="left", padx=2, pady=2)

        if not enabled:
            color = "yellow" if highlight else "red"
            t_color = "black" if highlight else "white"
            icon = ExclamationIcon(
                frame,
                size=16,
                circle_color=color,
                text_color=t_color,
                tooltip_text=tooltip_text or (
                    "Нельзя выбрать этот пункт, т.к. вы уже находитесь в нём" if highlight else "Действие сейчас недоступно"
                )
            )
            icon.pack(side="right", padx=5)

    def show(self, x_root, y_root):
        self.window.geometry(f"+{x_root}+{y_root}")

    def close_on_click_outside(self):
        def handler(event):
            try:
                x, y = event.x_root, event.y_root
                wx, wy = self.window.winfo_rootx(), self.window.winfo_rooty()
                ww, wh = self.window.winfo_width(), self.window.winfo_height()

                if not (wx <= x <= wx + ww and wy <= y <= wy + wh):
                    self.window.destroy()
            except Exception:
                pass

        self.window.after_idle(lambda: self.window.bind_all("<Button-1>", handler, add="+"))