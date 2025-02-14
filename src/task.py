"""
File name: task.py
Description: Contains logic related to tasks.

Author: Lacie Turner
Date created: 2025-02-10
Date last modified: 2025-02-13
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
from src.rank_tasks import rank_tasks


def load(task_file: Path) -> pd.DataFrame:
	"""Loads a task file into a pandas DataFrame."""
	task_file = Path(task_file)
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
		print(f"\n[INFO] Task added!\n")


def get_task_by_id(task_id: uuid.UUID, task_file: Path) -> pd.DataFrame:
	task_dataframe = load(task_file)
	single_task_dataframe = task_dataframe.loc[task_dataframe['id'] == task_id]

	return None if single_task_dataframe.empty else single_task_dataframe


def get_effort(task_id: uuid.UUID, task_file: Path) -> int:
	effort = 0
	task = get_task_by_id(task_id, task_file)
	if task is not None:
		effort = list(task.get('effort'))[0]

	return effort


def display_list(task_dataframe, start_index: int=0, end_index: int=-1) -> None:
	task_dataframe = task_dataframe[start_index:end_index]
	print(f"\n{'Task'.ljust(48)}"
	      f"{'Complete'.ljust(12)}"
	      f"{'Urgency'.ljust(11)}"
	      f"{'Importance'.ljust(14)}"
	      f"{'Effort'.ljust(10)}"
	      f"{'Due Date'.ljust(20)}")
	print("-" * 114)
	for index, row in task_dataframe.iterrows():
		print(f"{row['title'].ljust(48)}"
		      f"{'Y'.ljust(12) if row['complete'] == "FALSE" else 'N'.ljust(12)}"
		      f"{str(row['urgency']).ljust(11)}"
		      f"{str(row['importance']).ljust(14)}"
		      f"{str(row['effort']).ljust(10)}"
		      f"{str(row['due_date']).ljust(20) if row['due_date'] == row['due_date'] else '--'.ljust(20)}")
	print()


def display(task_id: uuid, task_file: Path) -> None:
	task = get_task_by_id(task_id, task_file)
	if task is not None:
		task = list(task.get('title'))[0]
		print(f"- {task}")


def rank(task_file: Path):
	tasks = load(task_file)
	return rank_tasks(tasks)
