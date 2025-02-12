"""
File name: task.py
Description: Defines the Task object.

Author: Lacie Turner
Date created: 2025-02-10
Date last modified: 2025-02-11
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
from pathlib import Path

CSV_FILE = Path("./data/generated-test-tasks.csv")


class Task:
	def __init__(self):
		pass


def load_tasks_from_csv(csv_file: Path = CSV_FILE) -> pd.DataFrame:
	task_df = pd.read_csv(csv_file)

	return task_df


def get_task_by_id(_id: uuid.UUID):
	pass


def get_all_tasks():
	pass


def get_complete_tasks():
	pass


def get_incomplete_tasks():
	pass


def get_task_suggestions(velocity: int):
	pass
