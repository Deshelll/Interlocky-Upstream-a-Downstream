import customtkinter as ctk

class ExclamationIcon(ctk.CTkCanvas):
    def __init__(self, master=None, size=16, bg_color="#1a1a1a", circle_color="red", text_color="white", tooltip_text=None, **kwargs):
        super().__init__(master, width=size, height=size, bg=bg_color, highlightthickness=0, **kwargs)
        self.size = size
        self.tooltip_text = tooltip_text
        self.tooltip_window = None

        radius = size // 2
        self.create_oval(1, 1, size-1, size-1, fill=circle_color, outline="")
        self.create_text(radius, radius, text="!", fill=text_color, font=("Segoe UI", int(size * 0.7), "bold"))

        if tooltip_text:
            self.bind("<Enter>", self.show_tooltip)
            self.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.tooltip_text:
            return

        x = self.winfo_rootx() + self.size + 4
        y = self.winfo_rooty() - 4

        self.tooltip_window = ctk.CTkToplevel(self)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.configure(fg_color="#333333")

        label = ctk.CTkLabel(self.tooltip_window, text=self.tooltip_text, text_color="white", fg_color="transparent", padx=8, pady=4, corner_radius=4)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
