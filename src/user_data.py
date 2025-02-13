"""
File name: user_data.py
Description: Handles user data.

Author: Lacie Turner
Date created: 2025-02-12
Date last modified: 2025-02-13
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
import src.task as task
from pathlib import Path

USER_DATA_FILE = Path("./data/user-data.json").resolve()
USER_TASK_FILE = Path("./data/user-tasks.csv").resolve()
USER_DATA_SCHEMA_FILE = Path("./data/__user-data-schema.json").resolve()


def load():
	if not USER_DATA_FILE.exists():
		print(f"[DEBUG] No user data file found")
		USER_DATA_FILE.touch()

	if USER_DATA_FILE.stat().st_size == 0:
		_data = json.loads(USER_DATA_SCHEMA_FILE.read_text(encoding="UTF-8")) # load schema
		USER_DATA_FILE.write_text(json.dumps(_data))
		print(f"[DEBUG] User data file generated at {USER_DATA_FILE}")

	user_data = json.loads(USER_DATA_FILE.read_text(encoding="UTF-8"))

	user_data["last_login"] = dt.datetime.now().isoformat()
	user_data["task_csv"] = str(USER_TASK_FILE)

	USER_DATA_FILE.write_text(json.dumps(user_data))

	return user_data


def greeting():
	user_data = load()
	print(f"\nHello{f', {user_data.get('username')}' if user_data.get('username') else ''}!\n")


def has_attr(attribute: str) -> bool:
	user_data = load()
	today = str(dt.date.today())
	return False if user_data.get(attribute).get(today) is None else True


def get_attr(attribute: str):
	user_data = load()
	if attribute in ['velocity', 'selected_tasks', 'completed_tasks', 'suggested_tasks', 'rejected_tasks']:
		today = str(dt.date.today())
		return user_data.get(attribute).get(today, [])
	return user_data.get(attribute, None)


def add_username(username: str):
	user_data = load()
	user_data["username"] = username
	USER_DATA_FILE.write_text(json.dumps(user_data))
	print(f"\n[INFO] Successfully {f'updated username to \'{username}\'' if username else 'removed username'}.")

	# re-greet them by the new name :)
	if username:
		greeting()


def add_velocity(velocity: int):
	user_data = load()
	today = str(dt.date.today())
	user_data["velocity"][today] = velocity
	USER_DATA_FILE.write_text(json.dumps(user_data))
	# print(f"[DEBUG] User velocity updated.")


def get_selected_effort() -> int:
	user_data = load()
	selected_tasks = get_attr('selected_tasks')

	selected_effort = 0
	for selected_task in selected_tasks:
		selected_effort += task.get_effort(selected_task, user_data.get('task_csv'))

	return selected_effort


def add_task(list_type: str, task_id: str):
	assert list_type in ["completed", "suggested", "rejected", "selected"], "Invalid list type"
	user_data = load()
	today = str(dt.date.today())

	if not user_data[f"{list_type}_tasks"].get(today):
		user_data[f"{list_type}_tasks"][today] = []

	if task_id not in user_data[f"{list_type}_tasks"][today]:
		user_data[f"{list_type}_tasks"][today].append(task_id)

	USER_DATA_FILE.write_text(json.dumps(user_data))
	print(f"[DEBUG] Added task {task_id} to {list_type}_tasks.")


def del_task(list_type: str, task_id: str):
	assert list_type in ["completed", "suggested", "rejected", "selected"], "Invalid list type"
	user_data = load()
	today = str(dt.date.today())

	if task_id in user_data[f"{list_type}_tasks"][today]:
		user_data[f"{list_type}_tasks"][today].remove(task_id)

	USER_DATA_FILE.write_text(json.dumps(user_data))


def display() -> None:
	user_data = load()
	today = str(dt.date.today())
	velocity = user_data.get("velocity").get(today)
	selected_tasks = user_data.get("selected_tasks").get(today)
	completed_tasks = user_data.get("completed_tasks").get(today)
	selected_effort = get_selected_effort()

	if velocity is None:
		print(f"You haven't entered your velocity for today, yet."
		      f"\nLet us know how much you feel you can do today by selecting 'Velocity' in the menu.")
	elif velocity == 0:
		print(f"I know you're busy today. Let's try again tomorrow! :)")
	elif velocity >= 1 and selected_tasks is None:
		print(f"You haven't selected any tasks for today. Select 'Suggest Tasks' in the menu to get started.")

	if velocity:
		if selected_tasks and completed_tasks is None:
			print(f"Here are your tasks for today:")
			for selected_task in selected_tasks:
				task.display(task_id=selected_task, task_file=user_data.get('task_csv'))

		if 0 < selected_effort < velocity:
			print("\nYou still have room to cross more off your list today! Select 'Suggest Tasks' in the menu to pick another task.")

	print()
