import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from menu import Menu


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "alarms.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_startup_load_listing_removal_and_persistence(self):
        self.storage_path.write_text(
            json.dumps([
                {"type": "ram", "target": 50},
                {"type": "cpu", "target": 90},
                {"type": "cpu", "target": 20},
            ]),
            encoding="utf-8",
        )
        menu = Menu(self.storage_path)
        output = StringIO()

        with patch("builtins.input", return_value="2"), redirect_stdout(output):
            menu.check(["3", "2", "4", "5"])

        displayed = output.getvalue()
        self.assertLess(displayed.index("1. Alarm - type: cpu, target: 20"),
                        displayed.index("2. Alarm - type: cpu, target: 90"))
        self.assertLess(displayed.index("2. Alarm - type: cpu, target: 90"),
                        displayed.index("3. Alarm - type: ram, target: 50"))
        self.assertIn("Alarm borttaget: Alarm - type: cpu, target: 90", displayed)
        self.assertEqual(
            json.loads(self.storage_path.read_text(encoding="utf-8")),
            [
                {"type": "ram", "target": 50},
                {"type": "cpu", "target": 20},
            ],
        )

        reloaded = Menu(self.storage_path)
        self.assertEqual(
            [(alarm.type, alarm.target) for alarm in reloaded.alarms],
            [("ram", 50), ("cpu", 20)],
        )

    def test_adding_alarm_and_exiting_saves_it(self):
        menu = Menu(self.storage_path)

        with patch("builtins.input", side_effect=["disk", "40"]), redirect_stdout(StringIO()):
            menu.check(["1", "5"])

        self.assertEqual(
            json.loads(self.storage_path.read_text(encoding="utf-8")),
            [{"type": "disk", "target": 40}],
        )


if __name__ == "__main__":
    unittest.main()