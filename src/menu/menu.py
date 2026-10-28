import sys
# Menu
# startar alarm skapande dialog
# options - add alarm, remove alarm, start monitor
# m = Monitor(Alarm(type, target), Alarm(type, target), Alarm(type, target))
# m.start(), m.stop()
# Startar monitor -> m.start()
# avslutar monitors arbete (ctrl c) -> m.stop()
# try:
#   m.start()
# except KeyboardInteruption:
#   m.stop() 
# handlar errors ?

class Menu:
  def check(self):
    print('menu')
  
  def __init__(self):
    self.args = sys.argv[1:]

  def run_args(self):
    # Make code to handle arguments
    # Check if arugments are valid
    try:
        if len(self.args) != 3:
          raise ValueError(f"Expected 3 arguments, got {len(self.args)}")

        # Convert and validate every argument (must be an integer 1-3)
        for i, arg in enumerate(self.args[:3]):
            try:
                number = int(arg)
            except ValueError:
                raise ValueError(f"Argument {i + 1} ('{arg}') is not a number")
            if number not in (1, 2, 3):
                raise ValueError(f"Argument {i + 1} is {number}, must be 1-3")

        if self.args[0] == 1:
            # Start monitor
            pass
        if self.args[1] == 2:
            # Choose alarm to monitor (cpu, ram, disk)
            pass
        if self.args[2] == 3:
            # Choose monitor limit percentage
            print("works here")

    except ValueError as e:
        print(f"Invalid arguments: {e}")
    
  # Christians del
  class StartupChoicesExhausted(Exception):
    pass

  def _read_input(self, prompt):
    if self.args:
      return self.args.pop(0)
    if self.non_interactive:
      raise self.StartupChoicesExhausted
    return input(prompt)

  def run(self):
    self.alarms = self._load_alarms()
    actions = {
      "1": ("Lägg till alarm", "add_alarm"),
      "2": ("Ta bort alarm", "remove_alarm"),
      "3": ("Lista alla konfigurerade alarm", "list_alarms"),
      "4": (
        "Skicka konfigurerade alarm till Monitoreringssystem",
        "save_alarms",
      ),
    }

    while True:
      print(
        "\nLarm-konfigurationssystem\n"
        "1. Lägg till alarm\n"
        "2. Ta bort alarm\n"
        "3. Lista alla konfigurerade alarm\n"
        "4. Skicka konfigurerade alarm till Monitoreringssystem\n"
        "5. Avsluta Larm-konfigurationssystem program"
      )
      choice = self._read_input("Välj ett alternativ: ").strip()

      if choice == "5":
        self.save_alarms()
        print("Larm-konfigurationssystemet avslutas.")
        return

      action = actions.get(choice)
      if action is None:
        print("Ogiltigt val. Välj ett alternativ mellan 1 och 5.")
        continue

      description, handler_name = action
      handler = getattr(self, handler_name, None)
      if handler is None:
        print(f"Funktionen '{description}' är ännu inte implementerad.")
        continue

      handler()

  def _alarm_file_path(self):
    from pathlib import Path

    return Path(__file__).resolve().parents[2] / "alarms" / "alarms.txt"

  def _load_alarms(self):
    from alarm import Alarm

    alarm_file = self._alarm_file_path()
    if not alarm_file.exists():
      return []

    alarms = []
    for line in alarm_file.read_text(encoding="utf-8").splitlines():
      if line.strip():
        alarms.append(Alarm(line.strip()))
    return alarms

  def add_alarm(self):
    from alarm import Alarm

    alarm_type = self._read_input("Ange kategori (cpu, ram eller disk): ").strip()
    target_input = self._read_input("Ange nivå (heltal 0-100): ").strip()
    try:
      target = int(target_input)
      alarm = Alarm(alarm_type, target)
    except ValueError as error:
      print(f"Alarmet kunde inte läggas till: {error}")
      return

    self.alarms.append(alarm)
    print(f"Alarm tillagt: {alarm}")

  def remove_alarm(self):
    sorted_alarms = sorted(
      self.alarms,
      key=lambda alarm: (alarm.type, alarm.target),
    )
    if not sorted_alarms:
      print("Det finns inga konfigurerade alarm att ta bort.")
      return

    self._print_alarms(sorted_alarms)
    try:
      index = int(self._read_input("Ange numret på alarmet som ska tas bort: ")) - 1
    except ValueError:
      print("Ange ett giltigt alarmnummer.")
      return

    if index < 0 or index >= len(sorted_alarms):
      print("Alarmnumret finns inte.")
      return

    alarm = sorted_alarms[index]
    self.alarms.remove(alarm)
    print(f"Alarm borttaget: {alarm}")

  def list_alarms(self):
    sorted_alarms = sorted(
      self.alarms,
      key=lambda alarm: (alarm.type, alarm.target),
    )
    if not sorted_alarms:
      print("Det finns inga konfigurerade alarm.")
      return

    self._print_alarms(sorted_alarms)

  def _print_alarms(self, alarms):
    for index, alarm in enumerate(alarms, start=1):
      print(f"{index}. {alarm}")

  def save_alarms(self):
    alarm_file = self._alarm_file_path()
    alarm_file.parent.mkdir(parents=True, exist_ok=True)
    contents = "\n".join(str(alarm) for alarm in self.alarms)
    if contents:
      contents += "\n"
    alarm_file.write_text(contents, encoding="utf-8")
    print("Alarmen har sparats till Monitoreringssystemet.")

  def start(self):
    self.non_interactive = bool(self.args)
    try:
      self.run()
    except self.StartupChoicesExhausted:
      print("Startup-valen tog slut innan programmet avslutades.")
      self.save_alarms()
