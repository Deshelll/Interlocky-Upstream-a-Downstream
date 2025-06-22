from ui.context_menu import CustomContextMenu

# Список всех кастомных выключателей
custom_switches = []  # каждый — словарь с info: canvas, id, pos, type

# === РЕГИСТРАЦИЯ ТРЁХПОЗИЦИОННОГО ВЫКЛЮЧАТЕЛЯ ===
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


# === РЕГИСТРАЦИЯ ДВУХПОЗИЦИОННОГО ВЫКЛЮЧАТЕЛЯ ===
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

# === МЕНЮ ДЛЯ ТРЁХПОЗИЦИОННОГО ===
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

        # 🔒 1. Первая и главная проверка – двухпозиционный включён
        if block_due_to_local_two:
            disabled = True
            tooltip = "Nelze operovat – vypínač ve stejném panelu je zapnutý"

        # ✅ Остальные проверки – только если не заблокировано выше
        if not disabled:
            if value == "on":
                conflict = is_group_conflict(switch, value)
                if conflict:
                    disabled = True
                    tooltip = conflict

            if (current == "on" and value == "short") or (current == "short" and value == "on"):
                disabled = True
                tooltip = "Přímý přechod mezi ON a Zazkratovat je zakázán – použijte mezipolohu"

        # 🔒 Если двухпозиционный включён

        # 🔒 Нельзя отключить ON, если другой в группе в short
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

        # 🔒 Проверка при включении (on), если сработал zkratovač с другой стороны
        if value == "on":
            if group in ("cabinet4", "cabinet5"):
                if any(sw["group_id"] == "cabinet3_left" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = "Nelze zapnout: levý zkratovač BC je aktivní"
            elif group in ("cabinet1", "cabinet2"):
                if any(sw["group_id"] == "cabinet3_right" and sw["position"] == "short" for sw in custom_switches):
                    disabled = True
                    tooltip = "Nelze zapnout: pravý zkratovač BC je aktivní"

        # 🔒 Обработка "Zazkratovat"
        if value == "short":
            # Найти связанную группу
            if group == "cabinet3_left":
                other_group = "cabinet3_right"
                excluded = {"cabinet4", "cabinet5"}
            elif group == "cabinet3_right":
                other_group = "cabinet3_left"
                excluded = {"cabinet1", "cabinet2"}
            else:
                other_group = group
                excluded = set()

            # Второй в паре
            other = [
                sw for sw in custom_switches
                if sw["type"] == "three"
                and sw is not switch
                and sw.get("group_id") == other_group
            ]

            if any(sw["position"] == "short" for sw in other):
                disabled = True
                tooltip = "Nelze zazkratovat: v tomto poli je již zkratováno"

            elif not any(sw["position"] == "on" for sw in other):
                disabled = True
                tooltip = "Zkratovat lze pouze pokud druhý spínač je ve stavu ON"

            elif any(
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




# === МЕНЮ ДЛЯ ДВУХПОЗИЦИОННОГО ===
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
        if value == "on":
            conflict = is_group_conflict(switch, value)
            if conflict:
                disabled = True
                tooltip = "Nelze zapnout, pokud je zapnutý druhý Incomer"
        # 🔒 Обрабатываем запрет выключения (off)
        if value == "off" and switch["position"] == "on":
            group = switch.get("group_id")

            if group in ("cabinet3_left", "cabinet3_right"):
                # Все трехпозиционные из cabinet3
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
                # В других шкафах: если трёхпозиционный в short
                three_in_short = any(
                    sw["type"] == "three"
                    and sw.get("group_id") == group
                    and sw["position"] == "short"
                    for sw in custom_switches
                )
                if three_in_short:
                    disabled = True
                    tooltip = "Vypnutí je možné pouze pomocí manuálního tlačítka, pokud jste ve stavu „Zazkratováno“."

        menu.add_option(
            label,
            command=lambda v=value: set_two_switch_position(switch, v),
            enabled=not is_current and not disabled,
            highlight=is_current,
            tooltip_text=tooltip
        )

    menu.show(event.x_root, event.y_root)
    menu.close_on_click_outside()



# === ОБНОВЛЕНИЕ ЛИНИИ (ТРЁХПОЗИЦИОННЫЙ) ===
def set_three_switch_position(switch, pos):
    canvas = switch["canvas"]
    x, y = switch["x"], switch["y"]
    current = switch["position"]

    # ❗ Запрет прямого перехода между on и short
    if (current == "on" and pos == "short") or (current == "short" and pos == "on"):
        # Вместо этого — только через "middle"
        return  # Ничего не делаем, можно подсветить/всплывающее — по желанию

    # ⏪ Если повторно выбирается текущее положение — не перерисовываем
    if current == pos:
        return

    # Удаляем старую линию
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


# === ОБНОВЛЕНИЕ ЛИНИИ (ДВУХПОЗИЦИОННЫЙ) ===
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
# Обновляем custom_switches, если объект заменился



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

    for sw in custom_switches:
        if sw.get("group_id") == other and sw["position"] == "on":
            return f"Nelze zapnout: { 'druhý' if other == 'cabinet4' else 'první' } Incomer je již aktivní"
    return False