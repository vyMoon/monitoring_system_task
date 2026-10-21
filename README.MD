# Project Setup and Installation

## 1. Clone the Repository

If SSH is configured:

    git clone git@git.chas-lab.dev:aleksei.popov/monitoring-system-with-interactive-configuration.git

If SSH is not configured:

    git clone https://git.chas-lab.dev/aleksei.popov/monitoring-system-with-interactive-configuration.git

## 2. Navigate to the Project Directory

    cd monitoring-system-with-interactive-configuration

## 3. Install the Project

Run the following command from the project root directory, where `pyproject.toml` is located:

    python -m pip install -e .

This installs the project in editable mode and allows Python to import project packages without specifying the `src` directory.

## 4. Verify the Import

    python -c "from alarm.alarm import Alarm; print(Alarm)"

If the command runs without errors, the `Alarm` class can be imported successfully.

## 5. Run the Project

Run the program from the project root directory:

    python index.py

The program stores configured alarms in `alarms.json` in the project root.
The same JSON file can be read by the monitoring system. It contains an array
of objects with a `type` and a numeric `target`.

Menu choices can be provided as command-line arguments to run them in order at
startup. For example, this lists the configured alarms and then exits:

    python index.py 3 5

If the sequence does not include choice `5`, the interactive menu continues
after the startup choices have been run. Adding an alarm still prompts for its
category and level.
