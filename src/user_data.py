"""
File name: user_data.py
Description: Handles user data.

Author: Lacie Turner
Date created: 2025-02-12
Date last modified: 2025-02-12
Python Version: 3.12
"""

__author__ = "Lacie Turner"
__maintainer__ = "Lacie Turner"
__email__ = "tasketai@lacie.dev"
__credits__ = ["Lacie Turner"]
__status__ = "Development"
__version__ = "0.0.1"

import json
import datetime as dt
from pathlib import Path

USER_DATA_FILE = Path("./data/user-data.json").resolve()
USER_TASK_FILE = Path("./data/user-tasks.csv").resolve()
USER_DATA_SCHEMA_FILE = Path("./data/__user-data-schema.json").resolve()


def load():
	if not USER_DATA_FILE.exists():
		print(f"[DEBUG] No user data file found")
		USER_DATA_FILE.touch()

	if USER_DATA_FILE.stat().st_size == 0:
		json_schema = json.loads(USER_DATA_SCHEMA_FILE.read_text(encoding="UTF-8")) # load schema
		USER_DATA_FILE.write_text(json.dumps(json_schema))  # write to file
		print(f"[DEBUG] User data file generated at {USER_DATA_FILE}")

	user_data = json.loads(USER_DATA_FILE.read_text(encoding="UTF-8"))
	user_data["last_login"] = dt.datetime.now().isoformat()
	USER_DATA_FILE.write_text(json.dumps(user_data))

	return user_data


def greeting():
	user_data = load()
	print(f"\nHello{f', {user_data.get('username')}' if user_data.get('username') else ''}!\n")


def has_attr(attribute: str) -> bool:
	user_data = load()
	today = str(dt.date.today())
	return False if user_data.get(attribute).get(today) is None else True


def add_velocity(velocity: int):
	user_data = load()
	today = str(dt.date.today())
	user_data["velocity"][today] = velocity
	USER_DATA_FILE.write_text(json.dumps(user_data))
	# print(f"[DEBUG] User velocity updated.")


def display() -> None:
	user_data = load()
	today = str(dt.date.today())
	velocity = user_data.get("velocity").get(today)
	selected_tasks = user_data.get("selected_tasks").get(today)
	completed_tasks = user_data.get("completed_tasks").get(today)

	if velocity is None:
		print(f"You haven't given a velocity for today."
		      f"\nLet us know how much you feel you can do today by selecting 'Velocity' in the menu.\n")
	elif velocity == 0:
		print(f"I know you're busy today. Let's try again tomorrow! :)\n")
	elif velocity >= 1 and selected_tasks is None:
		print(f"You haven't selected any tasks for today. Select 'Suggest Tasks' in the menu to get started.\n")
	elif selected_tasks and completed_tasks is None:
		print(f"Here are your tasks for today:\n")
		for task in selected_tasks:
			task.display(id=task)


def get_daily_velocity() -> int:
	pass
