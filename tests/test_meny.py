import sys
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
        self.alarm_path = Path(self.temp_dir.name) / "alarms.txt"
        with patch.object(sys, "argv", ["index.py"]):
            self.menu = Menu()
        self.menu._alarm_file_path = lambda: self.alarm_path

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_startup_sequence_adds_lists_and_saves_alarm(self):
        self.menu.args = ["1", "disk", "40", "3", "5"]
        output = StringIO()

        with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
            with redirect_stdout(output):
                self.menu.start()

        self.assertIn("Alarm tillagt: Alarm - type: disk, target: 40", output.getvalue())
        self.assertIn("1. Alarm - type: disk, target: 40", output.getvalue())
        self.assertEqual(
            self.alarm_path.read_text(encoding="utf-8"),
            "Alarm - type: disk, target: 40\n",
        )

    def test_loads_sorts_removes_and_saves_alarms(self):
        self.alarm_path.write_text(
            "Alarm - type: ram, target: 50\n"
            "Alarm - type: cpu, target: 90\n"
            "Alarm - type: cpu, target: 20\n",
            encoding="utf-8",
        )
        self.menu.args = ["3", "2", "2", "5"]
        output = StringIO()

        with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
            with redirect_stdout(output):
                self.menu.start()

        displayed = output.getvalue()
        self.assertLess(
            displayed.index("1. Alarm - type: cpu, target: 20"),
            displayed.index("2. Alarm - type: cpu, target: 90"),
        )
        self.assertLess(
            displayed.index("2. Alarm - type: cpu, target: 90"),
            displayed.index("3. Alarm - type: ram, target: 50"),
        )
        self.assertIn("Alarm borttaget: Alarm - type: cpu, target: 90", displayed)
        self.assertEqual(
            self.alarm_path.read_text(encoding="utf-8"),
            "Alarm - type: ram, target: 50\n"
            "Alarm - type: cpu, target: 20\n",
        )

    def test_invalid_choice_reprompts(self):
        self.menu.args = ["invalid", "5"]
        output = StringIO()

        with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
            with redirect_stdout(output):
                self.menu.start()

        self.assertIn("Ogiltigt val", output.getvalue())
        self.assertIn("Larm-konfigurationssystemet avslutas.", output.getvalue())

    def test_incomplete_startup_sequence_exits_without_prompting(self):
        self.menu.args = ["1"]
        output = StringIO()

        with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
            with redirect_stdout(output):
                self.menu.start()

        self.assertIn("Startup-valen tog slut innan programmet avslutades.", output.getvalue())
        self.assertEqual(self.alarm_path.read_text(encoding="utf-8"), "")

    def test_interactive_input_is_used_when_no_startup_choices(self):
        with patch("builtins.input", side_effect=["5"]) as mock_input:
            with redirect_stdout(StringIO()):
                self.menu.start()

        mock_input.assert_called_once_with("Välj ett alternativ: ")
        self.assertEqual(self.alarm_path.read_text(encoding="utf-8"), "")


if __name__ == "__main__":
    unittest.main()
