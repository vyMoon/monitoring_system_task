import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from alarm import Alarm
from menu import Menu


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "alarms.txt"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_startup_load_listing_removal_and_persistence(self):
        self.storage_path.write_text(
            "ram 50\ncpu 90\ncpu 20\n",
            encoding="utf-8",
        )
        menu = Menu(self.storage_path)
        output = StringIO()

        with patch("builtins.input", return_value="2"), redirect_stdout(output):
            menu.check(["3", "2", "2", "4", "5"])

        displayed = output.getvalue()
        self.assertLess(displayed.index("1. Alarm - type: cpu, target: 20"),
                        displayed.index("2. Alarm - type: cpu, target: 90"))
        self.assertLess(displayed.index("2. Alarm - type: cpu, target: 90"),
                        displayed.index("3. Alarm - type: ram, target: 50"))
        self.assertIn("Alarm borttaget: Alarm - type: cpu, target: 90", displayed)
        self.assertEqual(
            self.storage_path.read_text(encoding="utf-8"),
            "ram 50\ncpu 20\n",
        )

        reloaded = Menu(self.storage_path)
        self.assertEqual(
            [(alarm.type, alarm.target) for alarm in reloaded.alarms],
            [("ram", 50), ("cpu", 20)],
        )

    def test_adding_alarm_and_exiting_saves_it(self):
        menu = Menu(self.storage_path)

        with patch("builtins.input", side_effect=AssertionError("Unexpected interactive input")):
            with redirect_stdout(StringIO()):
                menu.check(["1", "disk", "40", "5"])

        self.assertEqual(
            self.storage_path.read_text(encoding="utf-8"),
            "disk 40\n",
        )

    def test_startup_choices_can_answer_all_prompts_without_input(self):
        menu = Menu(self.storage_path)

        with patch("builtins.input", side_effect=AssertionError("Unexpected interactive input")):
            menu.check(["1", "disk", "40", "3", "5"])

        self.assertEqual(
            self.storage_path.read_text(encoding="utf-8"),
            "disk 40\n",
        )

    def test_text_storage_preserves_float_targets(self):
        menu = Menu(self.storage_path)
        menu.alarms.append(Alarm("cpu", 1e-07))
        menu._save_alarms()

        reloaded = Menu(self.storage_path)
        self.assertEqual([(alarm.type, alarm.target) for alarm in reloaded.alarms], [
            ("cpu", 1e-07),
        ])


if __name__ == "__main__":
    unittest.main()