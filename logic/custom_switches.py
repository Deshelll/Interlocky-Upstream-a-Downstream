from ui.context_menu import CustomContextMenu
from logic import state

custom_switches = []


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
    switch["id"] = line

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
        ("on", "Zajet Disconnectorem"),
        ("middle", "Mezipoloha"),
        ("short", "Zazkratovat")
    ]

    for value, label in options:
        disabled = False
        tooltip = None
        highlight = (current == value)


        if block_due_to_local_two:
            disabled = True
            tooltip = "Nelze operovat – vypínač ve stejném panelu je zapnutý"


        if not disabled:
            if value == "on":
                conflict = is_group_conflict(switch, value)
                if conflict:
                    disabled = True
                    tooltip = conflict

            if (current == "on" and value == "short") or (current == "short" and value == "on"):
                disabled = True
                tooltip = "Přímý přechod mezi ON a Zazkratovat je zakázán – použijte mezipolohu"




        if group in ("cabinet3_left", "cabinet3_right") and current == "on" and value in ("middle", "short"):
            if any(
                sw["type"] == "three"
                and sw is not switch
                and sw.get("group_id") in ("cabinet3_left", "cabinet3_right")
                and sw["position"] == "short"
                for sw in custom_switches
            ):
                disabled = True
                tooltip = "Nelze vypnout – druhý třípolohový spínač je zkratován"


        if value == "on":
            if group in ("cabinet4", "cabinet5"):
                if any(sw["group_id"] == "cabinet3_left" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = "Nelze zapnout: levý zkratovač BC je aktivní"
            elif group in ("cabinet1", "cabinet2"):
                if any(sw["group_id"] == "cabinet3_right" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = "Nelze zapnout: pravý zkratovač BC je aktivní"


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
                    tooltip = "Nelze zazkratovat: v tomto poli je již zkratováno"
                elif not any(sw["position"] == "on" for sw in other):
                    disabled = True
                    tooltip = "Zkratovat lze pouze pokud druhý spínač je ve stavu ON"


            if not disabled:
                if any(
                    sw["type"] == "three"
                    and sw.get("group_id") in excluded
                    and sw["position"] == "on"
                    for sw in custom_switches
                ):
                    disabled = True
                    tooltip = "Zkratovat nelze, pokud v druhém rozvaděči je odpojovač zapnutý."



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
        ("on", "Zapnout"),
        ("off", "Vypnout")
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
                    tooltip = "Vypnutí je možné pouze pomocí manuálního tlačítka, pokud jste ve stavu „Zazkratováno“."
            else:

                three_in_short = any(
                    sw["type"] == "three"
                    and sw.get("group_id") == group
                    and sw["position"] == "short"
                    for sw in custom_switches
                )
                if three_in_short:
                    disabled = True
                    tooltip = "Vypnutí je možné pouze pomocí manuálního tlačítka, pokud jste ve stavu „Zazkratováno“."
        if value == "on":
            group = switch.get("group_id")
            if group in ("cabinet3_left", "cabinet3_right") and state.synchro_ui.visible:

                cab3_left_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
                    for sw in custom_switches
                )
                cab3_right_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
                    for sw in custom_switches
                )

                both_cabinet3_on = cab3_left_on and cab3_right_on

                if both_cabinet3_on:
                    mode = state.synchro_ui.mode_dropdown.get()

                    try:
                        left_val = float(state.synchro_ui.left_entries[0].get())
                        right_val = float(state.synchro_ui.right_entries[0].get())
                    except ValueError:
                        disabled = True
                        tooltip = "Neplatné hodnoty napětí"
                        continue

                    if mode == "DeadLine DeadBus":
                        if not (left_val == 0 and right_val == 0):
                            disabled = True
                            tooltip = "Obě napětí musí být nulová"

                    elif mode == "LiveLine DeadBus":
                        if not (left_val != 0 and right_val == 0):
                            disabled = True
                            tooltip = "Vlevo musí být napětí, vpravo nulové"

                    elif mode == "DeadLine LiveBus":
                        if not (left_val == 0 and right_val != 0):
                            disabled = True
                            tooltip = "Vlevo nulové, vpravo napětí"

                    elif mode == "LiveLine LiveBus":
                        try:
                            u_left = float(state.synchro_ui.left_entries[0].get())
                            f_left = float(state.synchro_ui.left_entries[1].get())
                            a_left = float(state.synchro_ui.left_entries[2].get())

                            u_right = float(state.synchro_ui.right_entries[0].get())
                            f_right = float(state.synchro_ui.right_entries[1].get())
                            a_right = float(state.synchro_ui.right_entries[2].get())
                        except ValueError:
                            disabled = True
                            tooltip = "Neplatné hodnoty parametrů"
                            continue

                        if not (
                            u_left == u_right and f_left == f_right and a_left == a_right and u_left != 0
                        ):
                            disabled = True
                            tooltip = "Parametry se musí shodovat a napětí ≠ 0"




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

                left_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_left" and sw["position"] == "on"
                    for sw in custom_switches
                )
                right_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == "cabinet3_right" and sw["position"] == "on"
                    for sw in custom_switches
                )
                two_on_bc = any(
                    sw["type"] == "two" and sw.get("group_id") in ("cabinet3_left", "cabinet3_right") and sw["position"] == "on"
                    for sw in custom_switches
                )


                local_three_on = any(
                    sw["type"] == "three" and sw.get("group_id") == group and sw["position"] == "on"
                    for sw in custom_switches
                )

                if other_three_on and other_two_on and left_three_on and right_three_on and two_on_bc and local_three_on:
                    if hasattr(state, "synchro_ui") and state.synchro_ui.visible:
                        mode = state.synchro_ui.mode_dropdown.get()
                        try:
                            u_left = float(state.synchro_ui.left_entries[0].get())
                            u_right = float(state.synchro_ui.right_entries[0].get())
                            f_left = float(state.synchro_ui.left_entries[1].get())
                            f_right = float(state.synchro_ui.right_entries[1].get())
                            a_left = float(state.synchro_ui.left_entries[2].get())
                            a_right = float(state.synchro_ui.right_entries[2].get())
                        except ValueError:
                            valid_sync = False
                        else:
                            match mode:
                                case "DeadLine DeadBus":
                                    valid_sync = u_left == 0 and u_right == 0
                                case "LiveLine DeadBus":
                                    valid_sync = u_left != 0 and u_right == 0
                                case "DeadLine LiveBus":
                                    valid_sync = u_left == 0 and u_right != 0
                                case "LiveLine LiveBus":
                                    valid_sync = (
                                        u_left == u_right and f_left == f_right and a_left == a_right and u_left != 0
                                    )
                                case _:
                                    valid_sync = False

                        if valid_sync:
                            disabled = False
                            tooltip = None
                    disabled = True
                    tooltip = "Nelze zapnout: oba Incomery by byly aktivní a rozvaděč BC je již celý zapnutý"



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
                    valid_sync = False
                    if hasattr(state, "synchro_ui") and state.synchro_ui.visible:
                        try:
                            u_left = float(state.synchro_ui.left_entries[0].get())
                            f_left = float(state.synchro_ui.left_entries[1].get())
                            a_left = float(state.synchro_ui.left_entries[2].get())
                            u_right = float(state.synchro_ui.right_entries[0].get())
                            f_right = float(state.synchro_ui.right_entries[1].get())
                            a_right = float(state.synchro_ui.right_entries[2].get())
                            mode = state.synchro_ui.mode_dropdown.get()

                            match mode:
                                case "DeadLine DeadBus":
                                    valid_sync = u_left == 0 and u_right == 0
                                case "LiveLine DeadBus":
                                    valid_sync = u_left != 0 and u_right == 0
                                case "DeadLine LiveBus":
                                    valid_sync = u_left == 0 and u_right != 0
                                case "LiveLine LiveBus":
                                    valid_sync = (
                                        u_left == u_right and f_left == f_right and a_left == a_right and u_left != 0
                                    )
                        except:
                            valid_sync = False

                    if not valid_sync:
                        disabled = True
                        tooltip = "Nelze zapnout: oba Incomery jsou plně zapnuté – nelze propojit rozvaděče"



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
            return "Nelze zapnout: druhý Incomer je již aktivní a BC je celý zapnutý"

        return "Incomer je již aktivní"



    return False
