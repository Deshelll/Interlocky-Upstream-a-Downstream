import customtkinter as ctk
from logic import state
from logic import custom_switches
from logic.custom_switches import custom_switches, set_two_switch_position
from ui.translations import t, switch_language

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

        
        self.labels = [t("label_voltage"), t("label_frequency"), t("label_angle")]
        defaults = ["0", "50", "0"]
        left_label = ctk.CTkLabel(self.left_column, text=t("tooltips_name_for_sync_1"), font=ctk.CTkFont(weight="bold"))
        left_label.pack(pady=(0, 5))

        right_label = ctk.CTkLabel(self.right_column, text=t("tooltips_name_for_sync_2"), font=ctk.CTkFont(weight="bold"))
        right_label.pack(pady=(0, 5))
        for label, default in zip(self.labels, defaults):
            self._add_row(self.left_column, label, default)
            self._add_row(self.right_column, label, default)



        self.mode_keys = {
            t("mode_both_dead"): "both_dead",
            t("mode_live_dead"): "live_dead",
            t("mode_dead_live"): "dead_live"
        }

        # Переведённые строки для показа
        mode_labels = list(self.mode_keys.keys())

        self.mode_dropdown = ctk.CTkOptionMenu(
            self.frame,
            values=mode_labels,
            command=lambda _: self.update_line_colors()
        )
        state.synchro_ui = self


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

        sync_ok = (
            u_left != 0 and u_right != 0 and
            u_left == u_right and
            f_left == f_right and
            a_left == a_right
        )

        selected_label = self.mode_dropdown.get()
        mode_key = self.mode_keys.get(selected_label, "unknown")

        match mode_key:
            case "both_dead":
                valid = (u_left == 0 and u_right == 0) or sync_ok
            case "live_dead":
                valid = (u_left != 0 and u_right == 0) or sync_ok
            case "dead_live":
                valid = (u_left == 0 and u_right != 0) or sync_ok
            case "live_live":
                valid = sync_ok
            case _:
                valid = False

        for name in (
            "synchro_input_left", "synchro_input_right",
            "synchro_bus_id", "synchro_bus_tail",
            "synchro_line_id", "synchro_line_tail",
            "synchro_bc_left", "synchro_bc_middle", "synchro_bc_right",
            "synchro_bridge"
        ):
            el = getattr(state, name, None)
            if el:
                state.canvas.itemconfig(el, fill="black", width=1)

        left_on = any(sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on" for sw in custom_switches)
        right_on = any(sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on" for sw in custom_switches)
        bc_two_on = any(sw["type"] == "two" and sw.get("group_id") in ("cabinet3_left", "cabinet3_right") and sw["position"] == "on" for sw in custom_switches)

        # === Трассировка от левой стороны (BUS), теперь от u_right
        if u_right != 0:
            clr = color(u_right, valid)
            reached = True
            for name in ("synchro_input_left", "synchro_bus_id", "synchro_bus_tail"):
                el = getattr(state, name, None)
                if el:
                    state.canvas.itemconfig(el, fill=clr, width=3)

            if reached and left_on:
                if state.synchro_bc_middle:
                    state.canvas.itemconfig(state.synchro_bc_middle, fill=clr, width=3)
            else:
                reached = False

            if reached and bc_two_on:
                for name in ("synchro_bc_left", "synchro_bc_right", "synchro_bridge"):
                    el = getattr(state, name, None)
                    if el:
                        state.canvas.itemconfig(el, fill=clr, width=3)
            else:
                reached = False

            if reached and right_on:
                for name in ("synchro_line_tail", "synchro_line_id", "synchro_input_right"):
                    el = getattr(state, name, None)
                    if el:
                        state.canvas.itemconfig(el, fill=clr, width=3)

        # === Трассировка от правой стороны (LINE), теперь от u_left
        if u_left != 0:
            clr = color(u_left, valid)
            reached = True
            for name in ("synchro_input_right", "synchro_line_tail", "synchro_line_id"):
                el = getattr(state, name, None)
                if el:
                    state.canvas.itemconfig(el, fill=clr, width=3)

            if reached and right_on:
                for name in ("synchro_bc_right", "synchro_bc_left", "synchro_bridge"):
                    el = getattr(state, name, None)
                    if el:
                        state.canvas.itemconfig(el, fill=clr, width=3)
            else:
                reached = False

            if reached and bc_two_on:
                if state.synchro_bc_middle:
                    state.canvas.itemconfig(state.synchro_bc_middle, fill=clr, width=3)
            else:
                reached = False

            if reached and left_on:
                for name in ("synchro_bus_id", "synchro_bus_tail", "synchro_input_left"):
                    el = getattr(state, name, None)
                    if el:
                        state.canvas.itemconfig(el, fill=clr, width=3)
