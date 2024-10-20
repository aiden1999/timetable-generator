# Timetable Generator Project

## Prerequisites
- Python 3: install from https://www.python.org/downloads, or download with your
OS's package manger, eg. Arch Linux and derivatives:
```
sudo pacman -S python3
```
Check that Python is added to PATH by typing (Arch)
```
python3
```
or (Windows)
```
python
```
into the terminal. If an error is returned, add to PATH.

## Installation
Download these 9 files:
- ./modules/crossover.py
- ./modules/fitness_function.py
- ./modules/ga.py
- ./modules/initial_population.py
- ./modules/mutation.py
- ./modules/selection.py
- data.json
- main.py
- settings.json (NOT the settings.json for VSCode, if applicable)
Make sure that the first 6 files are contained in the folder "modules", and that
that folder is in the same directory as the other 3 files.

## Configuration
Example input data is provided in data.json. Any changes/additions need to
follow the same pattern.
Parameters of the genetic algorithm can be changed in settings.json.

## Usage
Open the terminal to the containing directory and run main.py.
    `python3 ~/path/to/directory/main.py`         (Arch)
Or open main.py with Python IDLE and run (Windows).
