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

Run the required Python file from the project root directory.

