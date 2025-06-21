# Глобальные состояния переключателей
current_switch_state = "middle"
current_lower_switch_state = "middle"
current_middle_upper_state = "off"
current_middle_lower_state = "off"

# Разрешения на включение (как в script.py: .allowed = True)
set_middle_upper_position_allowed = True
set_middle_lower_position_allowed = True

# Текущее состояние напряжения
voltage_state = 0

# Постоянное аварийное событие
persistent_event = None

# Центр канваса (для зеркалирования и симметрии)
X_center = 200
Y_center = 210

# Элементы схемы (создаются при инициализации интерфейса)
switch_parts = []
lower_switch_parts = []
middle_upper_parts = []
middle_lower_parts = []

# Ссылка на canvas-индикатор напряжения (инициализируется в draw_schematic)
voltage_indicator = None

# Canvas может сохраняться здесь, если нужно к нему обращаться
canvas = None
