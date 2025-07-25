import os
import json
import tempfile

CONFIG_FILE = os.path.join(tempfile.gettempdir(), "interlocky_lang.json")

translations = {
    "cs": {
        "none": "Žadné blokování",
        "home": "Home",
        "task1": "Up/Downstream",
        "task2": "2 INC, 2 OUT, BC",
        "Manipulate": "Ovládání",
        "toggle_voltage": "Změnit napětí",
        "disable_upstream": "Vypnout Upstream",
        "disable_downstream": "Vypnout Downstream",
        "select_event": "Vyber událost:",
        "reset_lockout": "Reset Lockout",
        "language": "Jazyk",
        "oil_temp_alarm": "Oil_temp_Alarm",
        "oil_temp_trip": "Oil_temp_Trip",
        "w_temp_alarm": "W_temp_Alarm",
        "w_temp_trip": "W_temp_Trip",
        "pressure_relief": "Pressure_Relief",
        "pressure_alarm": "Pressure_Alarm",
        "pressure_trip": "Pressure_Trip",
        "level_alarm": "Level_Alarm",
        "level_trip": "Level_Trip",
        "buchholz_alarm": "Buchholz_Alarm",
        "buchholz_trip": "Buchholz_Trip",
        "i0_start": "I0_Start (tank)",
        "i0_trip": "I0_Trip (tank)",
        "silicagel_alarm": "Kvalita Silicagelu_Alarm",
        "choose": "Vyber",
        "reset": "Resetovat Lockout",
        "task2_title": "Ovládání",
        "disable_out_1": "Vypnout vypínač OUT 1",
        "disable_inc_1": "Vypnout vypínač INC 1",
        "disable_bc": "Vypnout vypínač BC",
        "disable_inc_2": "Vypnout vypínač INC 2",
        "disable_out_2": "Vypnout vypínač OUT 2",
        "synchrocheck": "Synchrocheck",
        "mode_both_dead": "Obě mrtvé",
        "mode_live_dead": "Živý přívod, mrtvá sběrnice",
        "mode_dead_live": "Mrtvý přívod, živá sběrnice",
        "label_voltage": "Napětí",
        "label_frequency": "Frekvence",
        "label_angle": "Úhel",
        "switch_on": "Disconnector On",
        "switch_middle": "Mezipoloha",
        "switch_short": "Zazkratovat",
        "tooltip_same_panel_on": "Nelze operovat – vypínač ve stejném panelu je zapnutý",
        "tooltip_direct_transition_blocked": "Přímý přechod mezi ON a Zazkratovat je zakázán – použijte mezipolohu",
        "tooltip_other_switch_shorted": "Nelze vypnout – druhý třípolohový spínač je zkratován",
        "tooltip_bc_right_on": "Nelze zapnout: pravý zkratovač BC je aktivní",
        "tooltip_already_earthed": "Nelze zazkratovat: v tomto poli je již zkratováno",
        "tooltip_earth_only_if_other_on": "Zkratovat lze pouze pokud druhý spínač je ve stavu ON",
        "tooltip_voltage_on_right": "Nelze zazkratovat: na pravé přípojnici je napětí",
        "tooltip_voltage_on_left": "Nelze zazkratovat: na levé přípojnici je napětí",
        "tooltip_other_disconnector_on": "Zkratovat nelze, pokud v druhém \nrozvaděči je odpojovač zapnutý.",
        "switch_on_2": "Zapnout",
        "switch_off_2": "Vypnout",
        "tooltip_manual_off_only_short": "Vypnutí je možné pouze pomocí manuálního tlačítka, \npokud jste ve stavu „Zazkratováno“.",
        "tooltip_invalid_voltage": "Neplatné hodnoty napětí",
        "tooltip_both_dead": "Na obou stranách nesmí být napětí, \nnebo je vyžadována plná synchronizace",
        "tooltip_live_dead": "Na busbaru musí být napětí a na lině  \nžádné, nebo je vyžadována plná synchronizace",
        "tooltip_dead_live": "Na lině  musí být napětí a na busbaru  \nžádné, nebo je vyžadována plná synchronizace",
        "tooltip_live_live": "Pro Live/Live musí být plná synchronizace",
        "tooltip_unknown_mode": "Neznámý režim",
        "tooltip_incomers_and_bc_active": "Nelze zapnout: oba Incomery by byly \naktivní a rozvaděč BC je již celý zapnutý",
        "tooltip_sync_blocked": "Nelze zapnout: oba Incomery jsou plně \nzapnuté – nelze propojit rozvaděče bez synchronizace",
        "tooltip_incomer_already_active": "Incomer je již aktivní",
        "tooltip_other_incomer_active": "Nelze zapnout: druhý Incomer \nje již aktivní a BC je celý zapnutý",
        "event_none": "Žadné blokování",
        "tooltip_already_in_position": "Jste již v této poloze",
        "switch_on": "Zajet Disconnectorem",
        "switch_middle": "Mezipoloha",
        "switch_short": "Zazkratovat",
        "tooltip_reset_required": "Resetujte Lockout",
        "tooltip_lower_on_block": "Nelze zazkratovat, pokud je \ndisconnector Downstream připojen k přípojnici",
        "tooltip_lower_short_block": "Nelze zapnout: Downstream \nzkratovač je zkratován",
        "tooltip_middle_upper": "Nelze vybrat: Upstream vypínač \nje již zapnutý",
        "tooltip_mid_back": "Nejdříve musíte vypnout vypínač",
        "tooltip_voltage_short": "Nelze zazkratovat, pokud je \nna kabelech napětí",
        "tooltip_on_short": "Nelze přeskočit mezipolohu \nmezi „Disconnector On“ a „Zazkratovat“",
        "tooltip_upper_on_block": "Nelze zazkratovat, \npokud je disconnector Upstream připojen k přípojnici",
        "tooltip_upper_short_block": "Nelze zapnout: Upstream zkratovač \nje zkratován",
        "tooltip_not_allowed": "Zapnutí je zakázáno",
        "tooltip_not_middle": "Nelze přeskočit mezipolohu \nmezi „Disconnector On“ a „Zazkratovat“",
        "tooltip_ml_on": "Downstream vypínač je v poloze „zapnuto“",
        "tooltip_ml_mid_block": "Nelze přepnout do mezipolohy — vypínač je aktivní.",
        "tooltip_lower_on_short": "Nejdříve musíte vypnout vypínač",
        "tooltip_short_block": "Odzkratujte pomocí manuálního tlačítka",
        "tooltip_mu_off": "Nejdříve musíte zapnout vypínač Upstream",
        "tooltip_voltage_block": "Na kabelech je napětí",
        "tooltip_all_on": "Všechny vypínače jsou zapnuté",
        "tooltip_already_in_position": "Jste již v této poloze",
        "tooltips_name_for_sync_1": "Line(Kabely)",
        "tooltips_name_for_sync_2": "Busbar(Přípojnice)",
    },
    "en": {
    "none": "No Blocking",
    "home": "Home",
    "task1": "Up/Downstream",
    "task2": "2 INC, 2 OUT, BC",
    "Manipulate": "Control",
    "language": "Language",
    "choose": "Select",
    "reset": "Reset Lockout",
    "toggle_voltage": "Change voltage",
    "disable_upstream": "Open Circuit \nBreaker in Upstream",
    "disable_downstream": "Open Circuit \nBreaker in Downstream",
    "select_event": "Select event:",
    "reset_lockout": "Reset Lockout",
    "oil_temp_alarm": "Oil Temperature Alarm",
    "oil_temp_trip": "Oil Temperature Trip",
    "w_temp_alarm": "Winding Temperature Alarm",
    "w_temp_trip": "Winding Temperature Trip",
    "pressure_relief": "Pressure Relief",
    "pressure_alarm": "Pressure Alarm",
    "pressure_trip": "Pressure Trip",
    "level_alarm": "Level Alarm",
    "level_trip": "Level Trip",
    "buchholz_alarm": "Buchholz Alarm",
    "buchholz_trip": "Buchholz Trip",
    "i0_start": "I0 Start (tank)",
    "i0_trip": "I0 Trip (tank)",
    "silicagel_alarm": "Silica Gel Quality Alarm",
    "task2_title": "Control",
    "disable_out_1": "Open Circuit \nBreaker in OUT 1",
    "disable_inc_1": "Open Circuit \nBreaker in INC 1",
    "disable_bc": "Open Circuit \nBreaker in BC",
    "disable_inc_2": "Open Circuit \nBreaker in INC 2",
    "disable_out_2": "Open Circuit \nBreaker in OUT 2",
    "synchrocheck": "Synchrocheck",
    "mode_both_dead": "Both Dead",
    "mode_live_dead": "LiveLine, DeadBus",
    "mode_dead_live": "DeadLine, DeadBus",
    "label_voltage": "Voltage",
    "label_frequency": "Frequency",
    "label_angle": "Angle",
    "switch_on": "Disconnector Close",
    "switch_middle": " Isolate Position",
    "switch_short": "Earth Switch Close",
    "switch_on_2": "Close",
    "switch_off_2": "Open",
    "tooltip_same_panel_on": "Cannot operate: Circuit Breaker in same panel is Closed",
    "tooltip_direct_transition_blocked": "Direct transition between Disconnector ON and Earth Switch On \nis prohibited – must be isolated first",
    "tooltip_already_in_position": "Already in this position",
    "tooltip_reset_required": "Reset lockout required",
    "tooltip_other_switch_shorted": "Cannot Close: other three-position Circuit Breaker is earthed",
    "tooltip_already_earthed": "Cannot Earth: bay is already earthed ",
    "tooltip_earth_only_if_other_on": "You can Earth if other Disconnector is in ON position",
    "tooltip_voltage_on_right": "Cannot Earth: voltage present on right busbar",
    "tooltip_voltage_on_left": "Cannot Earth: voltage present on left busbar",
    "tooltip_voltage_short": "Cannot Earth when voltage is present on cables",
    "tooltip_bc_right_on": "Cannot Open: right BC’s earth switch is earthed",
    "tooltip_other_disconnector_on": "Cannot Earth if Disconnector in other panel is On",
    "tooltip_manual_off_only_short": "Open only possible via manual button when in 'Earthed' state",
    "tooltip_short_block": " Open only possible via manual button when in 'Earthed' state",
    "tooltip_invalid_voltage": "Invalid voltage values",
    "tooltip_both_dead": "Both voltages must be zero or full synchronization",
    "tooltip_live_dead": "Voltage must be present on the Busbar side and absent on the Line side,\n or full synchronization is required",
    "tooltip_dead_live": "Voltage must be present on the Line side and absent on the Busbar side, \nor full synchronization is required",
    "tooltip_live_live": "Full synchronization of voltage, frequency, and angle is required \nwhen both Busbar and Line sides are energized",
    "tooltip_unknown_mode": "Unknown mode",
    "tooltip_incomers_and_bc_active": "Cannot Close: both incomers would be \nactive and BC panel is already fully Closed",
    "tooltip_sync_blocked": "Cannot Close: both incomers are fully Closes – cannot connect panels",
    "tooltip_incomer_already_active": "Incomer is already active",
    "tooltip_other_incomer_active": "Cannot Close: other incomer is already active \nand BC is fully Close",
    "tooltip_lower_on_block": "Cannot Earth if downstream disconnector is connected to busbar",
    "tooltip_lower_short_block": "Cannot Close: downstream Earth Switch is Earthed",
    "tooltip_upper_on_block": "Cannot Earth if upstream disconnector is connected to busbar",
    "tooltip_upper_short_block": "Cannot Close: upstream Earth Switch is Earthed",
    "tooltip_middle_upper": "Cannot select: upstream circuit breaker is already On",
    "tooltip_mid_back": "Must first Open the circuit breaker ",
    "tooltip_on_short": " Insulation cannot be missed between 'Disconnector Close' and 'Earthed'",
    "tooltip_not_middle": " Insulation cannot be missed between 'Disconnector Close' and 'Earthed",
    "tooltip_ml_on": "Downstream circuit breaker is in 'On' position",
    "tooltip_ml_mid_block": "Cannot be Opened — circuit breaker is On",
    "tooltip_lower_on_short": "Must first Close the circuit breaker ",
    "tooltip_mu_off": "Must first Close upstream circuit breaker ",
    "tooltip_not_allowed": "Open is prohibited",
    "tooltip_voltage_block": "Voltage present on cables",
    "tooltip_all_on": "All circuit breakeres are On",
    "event_none": "No blocking",
    "tooltips_name_for_sync_1": "Line (Cables)",
    "tooltips_name_for_sync_2": "Busbar",

    },
        "ru": {
        "none": "Нет блокировки",
        "home": "Главная",
        "task1": "Выше/нижестоящая \nсторона",
        "task2": "2 ввода, 2 вывода,\nсекционный \nвыключатель",
        "Manipulate": "Управление",
        "toggle_voltage": "Изменить напряжение",
        "disable_upstream": "Отключить \nвышестоящую сторону",
        "disable_downstream": "Отключить \nнижестоящую сторону",
        "select_event": "Выберите событие:",
        "reset_lockout": "Сброс блокировки",
        "language": "Язык",
        "oil_temp_alarm": "Предупреждение по температуре масла",
        "oil_temp_trip": "Авария по температуре масла",
        "w_temp_alarm": "Предупреждение по температуре обмотки",
        "w_temp_trip": "Авария по температуре обмотки",
        "pressure_relief": "Срабатывание предохранительного клапана",
        "pressure_alarm": "Предупреждение по давлению",
        "pressure_trip": "Авария по давлению",
        "level_alarm": "Предупреждение по уровню",
        "level_trip": "Авария по уровню",
        "buchholz_alarm": "Предупреждение Бухгольца",
        "buchholz_trip": "Авария Бухгольца",
        "i0_start": "Запуск по I0 (бак)",
        "i0_trip": "Авария по I0 (бак)",
        "silicagel_alarm": "Предупреждение по качеству силикагеля",
        "choose": "Выбрать",
        "reset": "Сбросить блокировку",
        "task2_title": "Управление",
        "disable_out_1": "Отключить \nвыключатель вывода 1",
        "disable_inc_1": "Отключить \nвыключатель ввода 1",
        "disable_bc": "Отключить \nсекционный выключатель",
        "disable_inc_2": "Отключить \nвыключатель ввода 2",
        "disable_out_2": "Отключить \nвыключатель вывода 2",
        "synchrocheck": "Синхронизм",
        "mode_both_dead": "Обе стороны обесточены",
        "mode_live_dead": "Питание подано / шина обесточена",
        "mode_dead_live": "Питание отсутствует / шина под напряжением",
        "label_voltage": "Напряжение",
        "label_frequency": "Частота",
        "label_angle": "Угол",
        "switch_on": "Разъединитель включён",
        "switch_middle": "Среднее положение",
        "switch_short": "Заземлитель включён",
        "tooltip_same_panel_on": "Операция невозможна — выключатель в том же шкафу включён",
        "tooltip_direct_transition_blocked": "Прямой переход между ВКЛ и Заземлением запрещён — \nиспользуйте среднее положение",
        "tooltip_other_switch_shorted": "Отключение невозможно — другой трёхпозиционный разъединитель заземлён",
        "tooltip_bc_right_on": "Включение невозможно: правый заземлитель BC активен",
        "tooltip_already_earthed": "Заземление невозможно: уже заземлено в этом шкафу",
        "tooltip_earth_only_if_other_on": "Заземление возможно только если другой разъединитель включён",
        "tooltip_voltage_on_right": "Заземление невозможно: на правой шине есть напряжение",
        "tooltip_voltage_on_left": "Заземление невозможно: на левой шине есть напряжение",
        "tooltip_other_disconnector_on": "Заземление невозможно, если в другом шкафу разъединитель включён",
        "switch_on_2": "Включить",
        "switch_off_2": "Отключить",
        "tooltip_manual_off_only_short": "Отключение возможно только вручную, если активен заземлитель",
        "tooltip_invalid_voltage": "Недопустимые значения напряжения",
        "tooltip_both_dead": "Оба напряжения должны быть равны нулю или полностью синхронизированы",
        "tooltip_live_dead": "Слева напряжение, справа — ноль, или полная синхронизация",
        "tooltip_dead_live": "Слева — ноль, справа напряжение, или полная синхронизация",
        "tooltip_live_live": "Для режима Live/Live требуется полная синхронизация",
        "tooltip_unknown_mode": "Неизвестный режим",
        "tooltip_incomers_and_bc_active": "Включение невозможно: оба ввода активны, \nа секционный выключатель уже включён",
        "tooltip_sync_blocked": "Включение невозможно: оба ввода уже включены — \nсоединение между без синхронизации \nними запрещено",
        "tooltip_incomer_already_active": "Ввод уже активен",
        "tooltip_other_incomer_active": "Включение невозможно: другой ввод активен и секционный выключатель включён",
        "event_none": "Нет блокировки",
        "tooltip_already_in_position": "Вы уже в этом положении",
        "tooltip_reset_required": "Требуется сброс блокировки",
        "tooltip_lower_on_block": "Заземление невозможно, если нижестоящий разъединитель подключён к шине",
        "tooltip_lower_short_block": "Включение невозможно: нижестоящий заземлитель активен",
        "tooltip_middle_upper": "Выбор невозможен: вышестоящий выключатель уже включён",
        "tooltip_mid_back": "Сначала отключите выключатель",
        "tooltip_voltage_short": "Нельзя заземлить, если на кабелях есть напряжение",
        "tooltip_on_short": "Нельзя перейти напрямую между ВКЛ и Заземлением — используйте среднее положение",
        "tooltip_upper_on_block": "Заземление невозможно, если вышестоящий разъединитель подключён к шине",
        "tooltip_upper_short_block": "Включение невозможно: вышестоящий заземлитель активен",
        "tooltip_not_allowed": "Включение запрещено",
        "tooltip_not_middle": "Нельзя перейти напрямую между ВКЛ и Заземлением — используйте среднее положение",
        "tooltip_ml_on": "Нижестоящий выключатель находится во включённом положении",
        "tooltip_ml_mid_block": "Переход в среднее положение невозможен — выключатель активен",
        "tooltip_lower_on_short": "Сначала необходимо отключить выключатель",
        "tooltip_short_block": "Отключите заземлитель вручную",
        "tooltip_mu_off": "Сначала включите вышестоящий выключатель",
        "tooltip_voltage_block": "На кабелях есть напряжение",
        "tooltip_all_on": "Все выключатели включены",
        "tooltips_name_for_sync_1": "Шина 2(Кабели)",
        "tooltips_name_for_sync_2": "Шина 1",
    },
}
current_language = "en"

def t(key):
    return translations[current_language].get(key, key)

def switch_language(to_lang):
    global current_language
    if to_lang in translations:
        current_language = to_lang
        save_language_choice(to_lang)

def get_current_language():
    return current_language

def save_language_choice(lang_code):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"language": lang_code}, f)
    except Exception as e:
        pass

def load_language_choice():
    global current_language
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lang = json.load(f).get("language")
                if lang in translations:
                    current_language = lang
    except Exception as e:
        pass