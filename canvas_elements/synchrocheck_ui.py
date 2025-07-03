import customtkinter as ctk
from logic import state
from logic import custom_switches
from logic.custom_switches import custom_switches, set_two_switch_position

class SynchroUI:
    def __init__(self, parent):

        self.left_entries = []
        self.right_entries = []
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.visible = False

        columns_frame = ctk.CTkFrame(self.frame)
        columns_frame.pack(pady=10)

        self.left_column = ctk.CTkFrame(columns_frame)
        self.right_column = ctk.CTkFrame(columns_frame)
        self.left_column.pack(side="left", padx=20)
        self.right_column.pack(side="left", padx=20)

        self.labels = ["Napětí", "Frekvence", "Úhel"]
        defaults = ["0", "50", "0"]

        for label, default in zip(self.labels, defaults):
            self._add_row(self.left_column, label, default)
            self._add_row(self.right_column, label, default)



        self.mode_dropdown = ctk.CTkOptionMenu(
            self.frame,
            values=[
                "DeadLine DeadBus",
                "LiveLine DeadBus",
                "DeadLine LiveBus",
                "LiveLine LiveBus"
            ],
            command=lambda _: self.update_line_colors()
        )

        self.mode_dropdown.pack(pady=(10, 5))

    def _add_row(self, parent, label_text, default_value=""):
        row = ctk.CTkFrame(parent)
        row.pack(pady=2)

        label = ctk.CTkLabel(row, text=label_text, width=80, anchor="e")
        entry = ctk.CTkEntry(row, width=100)
        entry.insert(0, default_value)
        entry.bind("<KeyRelease>", lambda e: self.update_line_colors())
        entry.bind("<FocusOut>", lambda e: self.update_line_colors())
        entry.bind("<Return>", lambda e: self.update_line_colors())


        label.pack(side="left", padx=(0, 5))
        entry.pack(side="left")


        if parent == self.left_column:
            self.left_entries.append(entry)
        elif parent == self.right_column:
            self.right_entries.append(entry)


    def toggle(self):
        if self.visible:
            self.frame.pack_forget()
            self.visible = False
        else:
            self.frame.pack(pady=10)
            self.visible = True
            self.update_line_colors()

    def update_line_colors(self):
        if not self.visible:
            return
        if not state.canvas:
            return

        try:
            u_left = float(self.left_entries[0].get())
            u_right = float(self.right_entries[0].get())
            f_left = float(self.left_entries[1].get())
            f_right = float(self.right_entries[1].get())
            a_left = float(self.left_entries[2].get())
            a_right = float(self.right_entries[2].get())
            mode = self.mode_dropdown.get()
        except ValueError:
            return

        def color(voltage, valid):
            if voltage == 0:
                return "black"
            return "#14f523" if valid else "red"

        # === проверка валидности
        match mode:
            case "DeadLine DeadBus":
                valid = u_left == 0 and u_right == 0
            case "LiveLine DeadBus":
                valid = u_left != 0 and u_right == 0
            case "DeadLine LiveBus":
                valid = u_left == 0 and u_right != 0
            case "LiveLine LiveBus":
                valid = (
                    u_left == u_right and
                    f_left == f_right and
                    a_left == a_right and
                    u_left != 0
                )
            case _:
                valid = False

        # === всегда перекрашиваем основные шины
        bus_color = color(u_left, valid)
        line_color = color(u_right, valid)

        if state.synchro_bus_id:
            state.canvas.itemconfig(state.synchro_bus_id, fill=bus_color, width=3 if bus_color != "black" else 1)
        if state.synchro_bus_tail:
            state.canvas.itemconfig(state.synchro_bus_tail, fill=bus_color, width=3 if bus_color != "black" else 1)
        if state.synchro_line_id:
            state.canvas.itemconfig(state.synchro_line_id, fill=line_color, width=3 if line_color != "black" else 1)
        if state.synchro_line_tail:
            state.canvas.itemconfig(state.synchro_line_tail, fill=line_color, width=3 if line_color != "black" else 1)

        # === логика по трёхпозиционникам
        left_on = any(
            sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
            for sw in custom_switches
        )
        right_on = any(
            sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
            for sw in custom_switches
        )
        bc_two_on = any(
            sw["type"] == "two" and sw.get("group_id") in ("cabinet3_left", "cabinet3_right") and sw["position"] == "on"
            for sw in custom_switches
        )
        # === линии внутри BC

# === synchro_bc_middle (отображает правую сторону, если она активна)
        if state.synchro_bc_middle:
            if left_on:
                val = color(u_left, valid)
            elif right_on and bc_two_on:
                val = color(u_right, valid)
            else:
                val = "black"
            state.canvas.itemconfig(state.synchro_bc_middle, fill=val, width=3 if val != "black" else 1)

        # === synchro_bc_left
        if state.synchro_bc_left:
            if right_on:
                val = color(u_right, valid)
            elif left_on and bc_two_on:
                val = color(u_left, valid)
            else:
                val = "black"
            state.canvas.itemconfig(state.synchro_bc_left, fill=val, width=3 if val != "black" else 1)

        # === synchro_bc_right — только при right_on
        if state.synchro_bc_right:
            if right_on:
                val = color(u_right, valid)
            elif left_on and bc_two_on:
                val = color(u_left, valid)
            else:
                val = "black"
            state.canvas.itemconfig(state.synchro_bc_right, fill=val, width=3 if val != "black" else 1)

        # === synchro_bridge
        if state.synchro_bridge:
            if right_on:
                val = color(u_right, valid)
            elif left_on and bc_two_on:
                val = color(u_left, valid)
            else:
                val = "black"
            state.canvas.itemconfig(state.synchro_bridge, fill=val, width=3 if val != "black" else 1)
                        # === Если хотя бы одна сторона заскратована, и есть напряжение, то открыть двухпозиционный BC
        left_short = state.bc_left_short
        right_short = state.bc_right_short


        voltage_present = u_left > 0 or u_right > 0

        # === Автоматическое отключение общего двухпозиционного BC
        if voltage_present:
            sw_bc = next(
                (s for s in custom_switches
                if s["type"] == "two"
                and s.get("group_id") in ("cabinet3_left", "cabinet3_right")
                and s["position"] == "on"),
                None
            )

            if sw_bc:
                if left_on and right_short and u_left > 0:
                    set_two_switch_position(sw_bc, "off")
                elif right_on and left_short and u_right > 0:
                    set_two_switch_position(sw_bc, "off")

