from ui.context_menu import CustomContextMenu
from logic import state
from ui.translations import t, switch_language


custom_switches = []

def get_synchro_voltage(side):
    if not hasattr(state, "synchro_ui") or not state.synchro_ui.visible:
        return 0.0

    try:
        if side == "left":
            return float(state.synchro_ui.left_entries[0].get())
        elif side == "right":
            return float(state.synchro_ui.right_entries[0].get())
    except ValueError:
        return 0.0

    return 0.0

def register_three_switch(canvas, x, y, group_id=None):
    switch = {
        "type": "three",
        "position": "middle",
        "canvas": canvas,
        "x": x,
        "y": y,
        "group_id": group_id
    }

    line = canvas.create_line(x - 20, y - 25, x, y, width=2)
    switch["id"] = line

    def on_click(event):
        show_three_switch_menu(event, switch)

    hitbox = canvas.create_rectangle(x - 30, y - 30, x + 10, y + 10, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(line, "<Button-1>", on_click)
    canvas.tag_bind(hitbox, "<Button-1>", on_click)

    custom_switches.append(switch)

def draw_cross(canvas, x, y, size=9, color="black", width=2):
    offset = size // 2
    canvas.create_line(x - offset, y - offset, x + offset, y + offset, fill=color, width=width)
    canvas.create_line(x - offset, y + offset, x + offset, y - offset, fill=color, width=width)


def register_two_switch(canvas, x, y, group_id=None):
    switch = {
        "type": "two",
        "position": "off",
        "canvas": canvas,
        "x": x,
        "y": y,
        "group_id": group_id
    }

    line = canvas.create_line(x - 20, y - 25, x, y, width=2)
    cross1 = canvas.create_line(x - 5, y - 30, x + 4, y - 22, width=2)
    cross2 = canvas.create_line(x - 5, y - 22, x + 4, y - 30, width=2)


    switch["id"] = line
    switch["cross"] = (cross1, cross2)

    def on_click(event):
        show_two_switch_menu(event, switch)

    hitbox = canvas.create_rectangle(x - 30, y - 30, x + 10, y + 10, fill="lightgray", stipple="gray25", outline="")
    canvas.tag_bind(line, "<Button-1>", on_click)
    canvas.tag_bind(hitbox, "<Button-1>", on_click)

    custom_switches.append(switch)


def show_three_switch_menu(event, switch):
    menu = CustomContextMenu(switch["canvas"])
    current = switch["position"]
    group = switch.get("group_id")

    if group in ("cabinet3_left", "cabinet3_right"):
        block_due_to_local_two = any(
            sw["type"] == "two"
            and sw["position"] == "on"
            and sw.get("group_id") in ("cabinet3_left", "cabinet3_right")
            for sw in custom_switches
        )
    else:
        block_due_to_local_two = any(
            sw["type"] == "two"
            and sw["position"] == "on"
            and sw.get("group_id") == group
            for sw in custom_switches
        )


    options = [
        ("on", t("switch_on")),
        ("middle", t("switch_middle")),
        ("short", t("switch_short"))
    ]

    for value, label in options:
        disabled = False
        tooltip = None
        highlight = (current == value)


        if block_due_to_local_two:
            disabled = True
            tooltip = t("tooltip_same_panel_on")


        if not disabled:
            if value == "on":
                conflict = is_group_conflict(switch, value)
                if conflict:
                    disabled = True
                    tooltip = conflict

            if (current == "on" and value == "short") or (current == "short" and value == "on"):
                disabled = True
                tooltip = t("tooltip_direct_transition_blocked")




        if group in ("cabinet3_left", "cabinet3_right") and current == "on" and value in ("middle", "short"):
            if any(
                sw["type"] == "three"
                and sw is not switch
                and sw.get("group_id") in ("cabinet3_left", "cabinet3_right")
                and sw["position"] == "short"
                for sw in custom_switches
            ):
                disabled = True
                tooltip = t("tooltip_other_switch_shorted")


        if value == "on":
            if group in ("cabinet4", "cabinet5"):
                if any(sw["group_id"] == "cabinet3_left" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = "Nelze zapnout: levý zkratovač BC je aktivní"
            elif group in ("cabinet1", "cabinet2"):
                if any(sw["group_id"] == "cabinet3_right" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = t("tooltip_bc_right_on")


        if value == "short":
            if group == "cabinet3_left":
                other_group = "cabinet3_right"
                excluded = {"cabinet4", "cabinet5"}
            elif group == "cabinet3_right":
                other_group = "cabinet3_left"
                excluded = {"cabinet1", "cabinet2"}
            else:
                other_group = None
                excluded = set()


            if group in ("cabinet3_left", "cabinet3_right"):
                other = [
                    sw for sw in custom_switches
                    if sw["type"] == "three"
                    and sw.get("group_id") == other_group
                ]

                if any(sw["position"] == "short" for sw in other):
                    disabled = True
                    tooltip = t("tooltip_already_earthed")
                elif not any(sw["position"] == "on" for sw in other):
                    disabled = True
                    tooltip = t("tooltip_earth_only_if_other_on")
            if group == "cabinet3_left":
                u_right = get_synchro_voltage("right")
                if u_right > 0:
                    disabled = True
                    tooltip = tooltip = t("tooltip_voltage_on_right")

            elif group == "cabinet3_right":
                u_left = get_synchro_voltage("left")
                if u_left > 0:
                    disabled = True
                    tooltip = t("tooltip_voltage_on_left")

            if not disabled:
                if any(
                    sw["type"] == "three"
                    and sw.get("group_id") in excluded
                    and sw["position"] == "on"
                    for sw in custom_switches
                ):
                    disabled = True
                    tooltip = t("tooltip_other_disconnector_on")



        menu.add_option(
            label,
            command=lambda v=value: set_three_switch_position(switch, v),
            enabled=not disabled and not highlight,
            highlight=highlight,
            tooltip_text=tooltip
        )

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()





def show_two_switch_menu(event, switch):
    menu = CustomContextMenu(switch["canvas"])
    options = [
        ("on", t("switch_on_2")),
        ("off", t("switch_off_2"))
    ]

    for value, label in options:
        is_current = (switch["position"] == value)
        disabled = False
        tooltip = None

        if value == "off" and switch["position"] == "on":
            group = switch.get("group_id")

            if group in ("cabinet3_left", "cabinet3_right"):

                three_switches = [
                    sw for sw in custom_switches
                    if sw["type"] == "three" and sw.get("group_id") in ("cabinet3_left", "cabinet3_right")
                ]
                one_in_short = any(sw["position"] == "short" for sw in three_switches)
                one_in_on = any(sw["position"] == "on" for sw in three_switches)

                if one_in_short and one_in_on:
                    disabled = True
                    tooltip = t("tooltip_manual_off_only_short")
            else:

                three_in_short = any(
                    sw["type"] == "three"
                    and sw.get("group_id") == group
                    and sw["position"] == "short"
                    for sw in custom_switches
                )
                if three_in_short:
                    disabled = True
                    tooltip = t("tooltip_manual_off_only_short")
        if value == "on":
            group = switch.get("group_id")
            if group in ("cabinet3_left", "cabinet3_right"):

                inc1_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet2" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc1_two_on = any(
                    sw["type"] == "two" and sw.get("group_id") == "cabinet2" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc2_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet4" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc2_two_on = any(
                    sw["type"] == "two" and sw.get("group_id") == "cabinet4" and sw["position"] == "on"
                    for sw in custom_switches
                )

                both_incomers_on = inc1_three_on and inc1_two_on and inc2_three_on and inc2_two_on
                cab3_left_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
                    for sw in custom_switches
                )
                cab3_right_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
                    for sw in custom_switches
                )

                if both_incomers_on and cab3_left_on and cab3_right_on:
                    if hasattr(state, "synchro_ui") and state.synchro_ui.visible:
                        try:
                            u_left = float(state.synchro_ui.left_entries[0].get())
                            u_right = float(state.synchro_ui.right_entries[0].get())
                            f_left = float(state.synchro_ui.left_entries[1].get())
                            f_right = float(state.synchro_ui.right_entries[1].get())
                            a_left = float(state.synchro_ui.left_entries[2].get())
                            a_right = float(state.synchro_ui.right_entries[2].get())

                            selected_label = state.synchro_ui.mode_dropdown.get()
                            mode_key = state.synchro_ui.mode_keys.get(selected_label, "unknown")

                            sync_ok = (
                                u_left != 0 and u_right != 0 and
                                u_left == u_right and
                                f_left == f_right and
                                a_left == a_right
                            )

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

                        except Exception:
                            valid = False

                        if not valid:
                            disabled = True
                            tooltip = t("tooltip_sync_blocked")

                    else:
                        # === Синхрочек не активен — запрещаем
                        disabled = True
                        tooltip = t("tooltip_sync_blocked")





            if group in ("cabinet2", "cabinet4"):
                other = "cabinet4" if group == "cabinet2" else "cabinet2"

                other_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == other and sw["position"] == "on"
                    for sw in custom_switches
                )
                other_two_on = any(
                    sw["type"] == "two" and sw.get("group_id") == other and sw["position"] == "on"
                    for sw in custom_switches
                )

                bc_left_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
                    for sw in custom_switches
                )
                bc_right_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
                    for sw in custom_switches
                )
                bc_cb_on = any(
                    sw["type"] == "two" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
                    for sw in custom_switches
                )

                bc_closed = bc_left_on and bc_right_on and bc_cb_on

                if other_three_on and other_two_on and bc_closed:
                    disabled = True
                    tooltip = t("tooltip_other_incomer_active")






            if group in ("cabinet3_left", "cabinet3_right"):
                inc1_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet2" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc1_two_on = any(
                    sw["type"] == "two" and sw.get("group_id") == "cabinet2" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc2_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet4" and sw["position"] == "on"
                    for sw in custom_switches
                )
                inc2_two_on = any(
                    sw["type"] == "two" and sw.get("group_id") == "cabinet4" and sw["position"] == "on"
                    for sw in custom_switches
                )

                if inc1_three_on and inc1_two_on and inc2_three_on and inc2_two_on:
                    try:
                        u_left = float(state.synchro_ui.left_entries[0].get())
                        u_right = float(state.synchro_ui.right_entries[0].get())
                        f_left = float(state.synchro_ui.left_entries[1].get())
                        f_right = float(state.synchro_ui.right_entries[1].get())
                        a_left = float(state.synchro_ui.left_entries[2].get())
                        a_right = float(state.synchro_ui.right_entries[2].get())

                        selected_label = state.synchro_ui.mode_dropdown.get()
                        mode_key = state.synchro_ui.mode_keys.get(selected_label, "unknown")

                        sync_ok = (
                            u_left != 0 and u_right != 0 and
                            u_left == u_right and
                            f_left == f_right and
                            a_left == a_right
                        )

                        match mode_key:
                            case "both_dead":
                                valid_sync = (u_left == 0 and u_right == 0) or sync_ok
                            case "live_dead":
                                valid_sync = (u_left != 0 and u_right == 0) or sync_ok
                            case "dead_live":
                                valid_sync = (u_left == 0 and u_right != 0) or sync_ok
                            case "live_live":
                                valid_sync = sync_ok
                            case _:
                                valid_sync = False

                    except Exception:
                        valid_sync = False

                    if not valid_sync:
                        disabled = True
                        tooltip = t("tooltip_sync_blocked")




        menu.add_option(
            label,
            command=lambda v=value: set_two_switch_position(switch, v),
            enabled=not is_current and not disabled,
            highlight=is_current,
            tooltip_text=tooltip
        )

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()




def set_three_switch_position(switch, pos):
    canvas = switch["canvas"]
    x, y = switch["x"], switch["y"]
    current = switch["position"]
    if pos == "short":
        if switch.get("group_id") == "cabinet3_left":
            state.bc_left_short = True
        elif switch.get("group_id") == "cabinet3_right":
            state.bc_right_short = True
    elif pos == "middle":
        if switch.get("group_id") == "cabinet3_left":
            state.bc_left_short = False
        elif switch.get("group_id") == "cabinet3_right":
            state.bc_right_short = False

    if (current == "on" and pos == "short") or (current == "short" and pos == "on"):

        return


    if current == pos:
        return


    canvas.delete(switch["id"])

    coords = {
        "on": (x, y - 25, x, y),
        "middle": (x - 20, y - 25, x, y),
        "short": (x - 40, y, x, y)
    }

    line = canvas.create_line(*coords[pos], width=2)
    canvas.tag_bind(line, "<Button-1>", lambda e: show_three_switch_menu(e, switch))

    switch["id"] = line
    switch["position"] = pos
    if hasattr(state, "synchro_ui") and state.synchro_ui and state.synchro_ui.visible:
        state.synchro_ui.update_line_colors()


def set_two_switch_position(switch, pos):
    canvas = switch["canvas"]
    canvas.delete(switch["id"])

    x, y = switch["x"], switch["y"]

    coords = {
        "off": (x - 20, y - 25, x, y),
        "on": (x, y - 25, x, y)
    }

    line = canvas.create_line(*coords[pos], width=2)
    canvas.tag_bind(line, "<Button-1>", lambda e: show_two_switch_menu(e, switch))

    switch["id"] = line
    switch["position"] = pos
    if hasattr(state, "synchro_ui") and state.synchro_ui.visible:
        state.synchro_ui.update_line_colors()





def force_turn_off_two_switches_by_group(group_id):
    for sw in custom_switches:
        if sw["type"] == "two" and sw.get("group_id") == group_id:
            set_two_switch_position(sw, "off")
            
def is_group_conflict(switch, new_pos):
    if new_pos != "on":
        return False

    group = switch.get("group_id")
    if group not in ("cabinet2", "cabinet4"):
        return False

    other = "cabinet4" if group == "cabinet2" else "cabinet2"


    left_three_on = any(
        sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
        for sw in custom_switches
    )
    right_three_on = any(
        sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
        for sw in custom_switches
    )
    bc_two_on = any(
        sw["type"] == "two" and sw.get("group_id") in ("cabinet3_left", "cabinet3_right") and sw["position"] == "on"
        for sw in custom_switches
    )

    bc_fully_on = left_three_on and right_three_on and bc_two_on


    other_three_on = any(
        sw["type"] == "three" and sw.get("group_id") == other and sw["position"] == "on"
        for sw in custom_switches
    )
    other_two_on = any(
        sw["type"] == "two" and sw.get("group_id") == other and sw["position"] == "on"
        for sw in custom_switches
    )


    if other_three_on and other_two_on and bc_fully_on:

        if switch.get("type") == "three":
            return False

        if switch.get("type") == "two":
            return t("tooltip_other_incomer_active")

        return t("tooltip_incomer_already_active")



    return False
