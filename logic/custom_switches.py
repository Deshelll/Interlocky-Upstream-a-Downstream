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

    # Проверка: есть ли включённый двухпозиционный в этом же шкафу (по group_id)
    block_due_to_local_two = any(
        sw["type"] == "two"
        and sw["position"] == "on"
        and sw.get("group_id") == switch.get("group_id")
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
        # 🔒 Блок: если в cabinet3 есть short, нельзя отключить текущий ON
        if switch.get("group_id") == "cabinet3" and current == "on" and value in ("middle", "short"):
            if any(
                sw["type"] == "three"
                and sw is not switch
                and sw.get("group_id") == "cabinet3"
                and sw["position"] == "short"
                for sw in custom_switches
            ):
                disabled = True
                tooltip = "Нельзя отключить: другой выключатель заскратован"
        # Блокируем прямой переход on <-> short
        if (current == "on" and value == "short") or (current == "short" and value == "on"):
            disabled = True
            tooltip = "Переход напрямую из 'вкл.' в 'заземление' запрещён — только через 'mezipoloha'"

        # Блокируем всё, если двухпозиционный в этом шкафу включён
        elif block_due_to_local_two:
            disabled = True
            tooltip = "Нельзя переключать: двухпозиционный в этом шкафу включён"
        elif value == "on":
            # 🔒 Запрет: если в cabinet3 уже есть 'short', нельзя включать "on" в других шкафах
            if switch.get("group_id") != "cabinet3":
                if any(
                    sw["type"] == "three"
                    and sw.get("group_id") == "cabinet3"
                    and sw["position"] == "short"
                    for sw in custom_switches
                ):
                    disabled = True
                    tooltip = "Нельзя включить: в большом шкафу уже есть 'заскратовано'"
        elif value == "short":
            group = switch.get("group_id")

            other_in_group = [
                sw for sw in custom_switches
                if sw["type"] == "three"
                and sw is not switch
                and sw.get("group_id") == group
            ]

            # 🔐 Условие 1 — в группе уже есть short
            if any(sw["position"] == "short" for sw in other_in_group):
                disabled = True
                tooltip = "В группе уже один выключатель в 'заскратовать'"

            # 🔐 Только для cabinet3: второй должен быть включён + остальные выключены
            elif group == "cabinet3":
                # 2. Второй в группе не включён
                if not any(sw["position"] == "on" for sw in other_in_group):
                    disabled = True
                    tooltip = "Заскратовать можно только если второй выключатель включён (ON)"

                # 3. В других шкафах есть включённые
                elif any(
                    sw["type"] == "three"
                    and sw.get("group_id") != "cabinet3"
                    and sw["position"] == "on"
                    for sw in custom_switches
                ):
                    disabled = True
                    tooltip = "Заскратовать нельзя: в другом шкафу выключатель уже включён"
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

        # 🔒 Обрабатываем запрет выключения (off)
        if value == "off" and switch["position"] == "on":
            group = switch.get("group_id")

            if group == "cabinet3":
                # Все трехпозиционные из cabinet3
                three_switches = [
                    sw for sw in custom_switches
                    if sw["type"] == "three" and sw.get("group_id") == "cabinet3"
                ]
                one_in_short = any(sw["position"] == "short" for sw in three_switches)
                one_in_on = any(sw["position"] == "on" for sw in three_switches)

                if one_in_short and one_in_on:
                    disabled = True
                    tooltip = "Нельзя выключить: другой выключатель заскратован и один включён"
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
                    tooltip = "Нельзя выключить: заскратовано — отключите вручную"

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


def force_turn_off_two_switches_by_group(group_id):
    for sw in custom_switches:
        if sw["type"] == "two" and sw.get("group_id") == group_id:
            set_two_switch_position(sw, "off")