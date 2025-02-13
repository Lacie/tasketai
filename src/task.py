"""
File name: task.py
Description: Defines the Task object.

Author: Lacie Turner
Date created: 2025-02-10
Date last modified: 2025-02-12
Python Version: 3.12
"""

__author__ = "Lacie Turner"
__maintainer__ = "Lacie Turner"
__email__ = "tasketai@lacie.dev"
__credits__ = ["Lacie Turner"]
__status__ = "Development"
__version__ = "0.0.1"

import uuid
import pandas as pd
import datetime as dt
from pathlib import Path


class Task:
	def __init__(self):
		pass


def load(task_file: Path) -> pd.DataFrame:
	"""Loads a task file into a pandas DataFrame."""
	assert task_file.exists(), f"Task file does not exist at {task_file}"
	task_df = pd.read_csv(task_file)

	return task_df


def is_valid_title(title: str) -> bool:
	if not title.strip() or len(title.strip()) > 256:
		return False
	return True


def add(title: str, urgency: int, importance: int, effort: int, csv_file: Path) -> None:
	if csv_file.exists() and csv_file.stat().st_size > 0:
		with open(csv_file, "a") as f:
			now = dt.datetime.now().isoformat()
			#id,complete,title,urgency,importance,effort,due_date,_created,_modified
			f.write(f"{uuid.uuid4()},FALSE,{title},{urgency},{importance},{effort},,{now},{now}\n")
		print(f"\nTask added!\n")


def get_task_by_id(_id: uuid.UUID):
	pass


def get_all_tasks():
	pass


def get_complete_tasks():
	pass


def get_incomplete_tasks():
	pass


def get_task_suggestions(velocity: int, ranked_dataframe: pd.DataFrame) -> pd.DataFrame:
	assert velocity in range(1, 3), "Velocity must be between 1 and 3"
	pass


def display_list(task_dataframe, start_index: int=0, end_index: int=-1) -> None:
	task_df = task_dataframe[start_index:end_index]
	print(f"\n{'Task'.ljust(48)}"
	      f"{'Complete'.ljust(12)}"
	      f"{'Urgency'.ljust(11)}"
	      f"{'Importance'.ljust(14)}"
	      f"{'Effort'.ljust(10)}"
	      f"{'Due Date'.ljust(20)}")
	print("-" * 114)
	for index, row in task_df.iterrows():
		print(f"{row['title'].ljust(48)}"
		      f"{'Y'.ljust(12) if row['complete'] == "FALSE" else 'N'.ljust(12)}"
		      f"{str(row['urgency']).ljust(11)}"
		      f"{str(row['importance']).ljust(14)}"
		      f"{str(row['effort']).ljust(10)}"
		      f"{str(row['due_date']).ljust(20) if row['due_date'] == row['due_date'] else '--'.ljust(20)}")
	print()


def display(task_id: uuid, task_csv: Path) -> None:
	task_dataframe = load(task_csv)
	task = task_dataframe.loc[task_dataframe['id'] == task_id]
	print(task)