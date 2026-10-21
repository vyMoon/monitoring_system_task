import json
from pathlib import Path

from alarm import Alarm


class Menu:
    STORAGE_PATH = Path(__file__).resolve().parents[2] / "alarms.json"

    def __init__(self, storage_path=None):
        self.storage_path = Path(storage_path or self.STORAGE_PATH)
        self.alarms = self._load_alarms()

    def check(self, startup_choices=None):
        startup_choices = iter(startup_choices or [])

        while True:
            self._print_menu()
            try:
                choice = next(startup_choices)
            except StopIteration:
                choice = input("Välj ett alternativ: ").strip()

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

    def _add_alarm(self):
        alarm_type = input("Ange kategori (cpu, ram eller disk): ").strip()
        target_input = input("Ange nivå (0-100): ").strip()

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
        index_input = input("Ange numret på alarmet som ska tas bort: ").strip()
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

        alarm_data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        if not isinstance(alarm_data, list):
            raise ValueError("Alarmfilen måste innehålla en JSON-lista.")

        alarms = []
        for item in alarm_data:
            if not isinstance(item, dict) or "type" not in item or "target" not in item:
                raise ValueError("Varje alarm måste innehålla 'type' och 'target'.")
            alarms.append(Alarm(item["type"], item["target"]))
        return alarms

    def _save_alarms(self):
        alarm_data = [
            {"type": alarm.type, "target": alarm.target}
            for alarm in self.alarms
        ]
        self.storage_path.write_text(
            json.dumps(alarm_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
