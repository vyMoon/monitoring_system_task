from pathlib import Path

from alarm import Alarm


class Menu:
    STORAGE_PATH = Path(__file__).resolve().parents[2] / "alarms.txt"

    def __init__(self, storage_path=None):
        self.storage_path = Path(storage_path or self.STORAGE_PATH)
        self.alarms = self._load_alarms()

    def check(self, startup_choices=None):
        self._startup_choices = iter(startup_choices or [])

        while True:
            self._print_menu()
            choice = self._read_input("Välj ett alternativ: ")

            if choice == "1":
                self._add_alarm()
            elif choice == "2":
                self._remove_alarm()
            elif choice == "3":
                self._list_alarms()
            elif choice == "4":
                self._save_alarms()
                print("Alarmen har skickats till Monitoreringssystemet.")
            elif choice == "5":
                self._save_alarms()
                print("Larm-konfigurationssystemet avslutas.")
                return
            else:
                print("Ogiltigt val. Välj ett alternativ mellan 1 och 5.")

    def _print_menu(self):
        print(
            "Larm-konfigurationssystem\n"
            "1. Lägg till alarm\n"
            "2. Ta bort alarm\n"
            "3. Lista alla konfigurerade alarm\n"
            "4. Skicka konfigurerade alarm till Monitoreringssystem\n"
            "5. Avsluta Larm-konfigurationssystem program"
        )

    def _read_input(self, prompt):
        try:
            return next(self._startup_choices).strip()
        except StopIteration:
            return input(prompt).strip()

    def _add_alarm(self):
        alarm_type = self._read_input("Ange kategori (cpu, ram eller disk): ")
        target_input = self._read_input("Ange nivå (0-100): ")

        try:
            target = float(target_input) if "." in target_input else int(target_input)
            alarm = Alarm(alarm_type, target)
        except ValueError as error:
            print(f"Alarmet kunde inte läggas till: {error}")
            return

        self.alarms.append(alarm)
        print(f"Alarm tillagt: {alarm}")

    def _remove_alarm(self):
        sorted_alarms = self._sorted_alarms()
        if not sorted_alarms:
            print("Det finns inga konfigurerade alarm att ta bort.")
            return

        self._print_alarms(sorted_alarms)
        index_input = self._read_input("Ange numret på alarmet som ska tas bort: ")
        try:
            index = int(index_input) - 1
        except ValueError:
            print("Ange ett giltigt alarmnummer.")
            return

        if index < 0 or index >= len(sorted_alarms):
            print("Alarmnumret finns inte.")
            return

        alarm = sorted_alarms[index]
        self.alarms.remove(alarm)
        print(f"Alarm borttaget: {alarm}")

    def _list_alarms(self):
        sorted_alarms = self._sorted_alarms()
        if not sorted_alarms:
            print("Det finns inga konfigurerade alarm.")
            return

        self._print_alarms(sorted_alarms)

    def _sorted_alarms(self):
        return sorted(self.alarms, key=lambda alarm: (alarm.type, alarm.target))

    def _print_alarms(self, alarms):
        for index, alarm in enumerate(alarms, start=1):
            print(f"{index}. {alarm}")

    def _load_alarms(self):
        if not self.storage_path.exists():
            return []

        alarms = []
        for line_number, line in enumerate(
            self.storage_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            fields = line.split()
            if not fields:
                continue
            if len(fields) != 2:
                raise ValueError(
                    f"Ogiltigt format på rad {line_number} i alarmfilen."
                )

            alarm_type, target_input = fields
            try:
                try:
                    target = int(target_input)
                except ValueError:
                    target = float(target_input)
                alarms.append(Alarm(alarm_type, target))
            except ValueError as error:
                raise ValueError(
                    f"Ogiltigt alarm på rad {line_number} i alarmfilen: {error}"
                ) from error
        return alarms

    def _save_alarms(self):
        self.storage_path.write_text(
            "".join(f"{alarm.type} {alarm.target}\n" for alarm in self.alarms),
            encoding="utf-8",
        )
