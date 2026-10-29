# Team Contributions

    Jacqueline Cummings - Alarm class
    Christian Arroyo
    Julian Carlos Miguel Gacusan Agonoy
    Aleksei Popov - Monitor, Logger classes

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

Menu choices and answers to their prompts can be provided as command-line
arguments in order at startup. For example, this adds a disk alarm at level 40,
lists the configured alarms, and exits without interactive input:

    python index.py 1 disk 40 3 5

If the sequence does not include choice `5`, or does not provide all answers
required by its menu choices, the program continues interactively after using
the supplied arguments.
