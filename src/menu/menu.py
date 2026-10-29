import sys
from pathlib import Path
from logger.logger import Logger
from monitor.monitor import Monitor

# Ren funktion: returnerar en sorterad lista utan att ändra originalet.
# Lambda ger sorted en sorteringsnyckel; därför är sorted en högre ordningens funktion här.
def sort_alarms(alarms):
  return sorted(alarms, key=lambda alarm: (alarm.type, alarm.target))


# Christians kompletteringsdel
# Ren funktion: omvandlar alarmvärden till text utan utskrift eller ändring av indata.
def format_alarms(alarms: tuple[tuple[str, int | float], ...]) -> str:
  return "\n".join(
    f"{index}. Alarm - type: {alarm_type}, target: {target}"
    for index, (alarm_type, target) in enumerate(alarms, start=1)
  )

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
  """prefix for logging"""
  prefix = 'Menu'

  def check(self):
    print('menu')
  
  def __init__(self):
    self.args = sys.argv[1:]
    self.logger = self.get_logger()

  """creates and returns logger"""
  def get_logger(self) -> Logger:
    return Logger(Path.cwd())

  """send the information to logger with menu prefix"""
  def log(self, message: str):
    self.logger.logPrefix(self.prefix, message)

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
        "start_monitor",
      ),
      "5": ('Spara alarm', 'save_alarms')
    }

    while True:
      print(
        "\nLarm-konfigurationssystem\n"
        "1. Lägg till alarm\n"
        "2. Ta bort alarm\n"
        "3. Lista alla konfigurerade alarm\n"
        "4. Skicka konfigurerade alarm till Monitoreringssystem\n"
        "5. Spara alarm\n"
        "6. Avsluta Larm-konfigurationssystem program"
      )
      choice = self._read_input("Välj ett alternativ: ").strip()

      if choice == "6":
        print("Larm-konfigurationssystemet avslutas.")
        self.log('session finished')
        return

      action = actions.get(choice)
      if action is None:
        print("Ogiltigt val. Välj ett alternativ mellan 1 och 5.")
        continue

      description, handler_name = action
      self.log(f"user's choice: {description} ({handler_name})")
      handler = getattr(self, handler_name, None)
      if handler is None:
        print(f"Funktionen '{description}' är ännu inte implementerad.")
        self.log('functionality is not ready yet')
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
    self.log('Alarm configuration started')
    from alarm import Alarm

    alarm_type = self._read_input("Ange kategori (cpu, ram eller disk): ").strip()
    target_input = self._read_input("Ange nivå (heltal 0-100): ").strip()
    self.log(f"user's choice type: {alarm_type}, target: {target_input}")

    try:
      target = int(target_input)
      alarm = Alarm(alarm_type, target)
      self.log(f'alarm: {alarm} created')
    except ValueError as error:
      print(f"Alarmet kunde inte läggas till: {error}")
      self.log(error)
      return

    self.alarms.append(alarm)
    self.log('alarm saved')
    print(f"Alarm tillagt: {alarm}")

  def remove_alarm(self):
    self.log('alarm removal started')
    sorted_alarms = sort_alarms(self.alarms)
    if not sorted_alarms:
      print("Det finns inga konfigurerade alarm att ta bort.")
      self.log('there is no alarm in the system')
      return

    self._print_alarms(sorted_alarms)
    try:
      index = int(self._read_input("Ange numret på alarmet som ska tas bort: ")) - 1
    except ValueError:
      print("Ange ett giltigt alarmnummer.")
      return

    if index < 0 or index >= len(sorted_alarms):
      print("Alarmnumret finns inte.")
      self.log('alarm does not exist')
      return

    alarm = sorted_alarms[index]
    self.log(f'chosen alarm {alarm}')
    self.alarms.remove(alarm)
    self.log(f'alarm {alarm} removed')
    print(f"Alarm borttaget: {alarm}")

  def list_alarms(self):
    sorted_alarms = sort_alarms(self.alarms)
    if not sorted_alarms:
      print("Det finns inga konfigurerade alarm.")
      return

    self._print_alarms(sorted_alarms)

  def _print_alarms(self, alarms):
    self.log('existing alarms')
    alarm_values = tuple((alarm.type, alarm.target) for alarm in alarms)
    alarms_to_print = format_alarms(alarm_values)
    print(alarms_to_print)
    self.log(alarms_to_print)

  def save_alarms(self):
    self.log('alarm preservation')
    alarm_file = self._alarm_file_path()
    alarm_file.parent.mkdir(parents=True, exist_ok=True)
    contents = "\n".join(str(alarm) for alarm in self.alarms)
    self.log(f'alarm list: {contents}')
    if contents:
      contents += "\n"
    alarm_file.write_text(contents, encoding="utf-8")
    self.log('alarms saved')
    print("Alarmen har sparats till Monitoreringssystemet.")

  def start(self):
    self.non_interactive = bool(self.args)
    self.log('session started')
    try:
      self.run()
    except self.StartupChoicesExhausted as e:
      print("Startup-valen tog slut innan programmet avslutades.")
      self.log(f'{e}')
      self.save_alarms()

  def get_monitor(self) -> Monitor:
    return Monitor(
      self._alarm_file_path(),
      self.logger
    )

  def get_monitoring_time(self) -> str:
    return self._read_input(
      'Ange övervakningstid i sekunder. Om ingen tid anges är övervakningen obegränsad.'
    )

  def start_monitor(self):
    self.log('Monitoring started')
    self.save_alarms()
    monitor = self.get_monitor()
    sec =self.get_monitoring_time()

    try:
      try:
        time = int(sec)
        self.log(f'monitoring time {time}')
        monitor.startMonitor(time)
      except:
        self.log('infinity monitor')
        monitor.startMonitor()
    except KeyboardInterrupt:
      print('Monitorering avlutades')
      self.log('User has interrupted monitoring')
      return
    
    self.log('Monitoring finished')
