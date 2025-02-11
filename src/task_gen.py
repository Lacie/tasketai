"""
File name: task_gen.py
Description: Generates random tasks for testing purposes.

Author: Lacie Turner
Date created: 2025-02-10
Date last modified: 2025-02-10
Python Version: 3.12
"""

__author__ = "Lacie Turner"
__maintainer__ = "Lacie Turner"
__email__ = "tasketai@lacie.dev"
__credits__ = ["Lacie Turner"]
__status__ = "Development"
__version__ = "0.0.1"

import csv
import uuid
import random
from pathlib import Path
from datetime import datetime, timedelta

CSV_FILE = Path("../data/generated-test-tasks.csv")
NUM_TASKS = 250
MIN_DUE_DATE = datetime.now() - timedelta(days=5)
MAX_DUE_DATE = datetime.now() + timedelta(days=35)
DUE_DATE_PROBABILITY = random.uniform(0.08, 0.16)


def generate_tasks(num_tasks: int, min_due_date: datetime = MIN_DUE_DATE, max_due_date: datetime = MAX_DUE_DATE,
                   due_date_probability: float = DUE_DATE_PROBABILITY):
	"""
	Generates a list of tasks based on the given parameters.

	:param num_tasks: The number of tasks to generate.
	:param min_due_date: The minimum due date to consider.
	:param max_due_date: The maximum due date to consider.
	:param due_date_probability: The probability to consider due date.
	:return: The list of generated tasks.
	"""
	tasks = []
	for num in range(num_tasks):
		task_id = str(uuid.uuid4())
		complete = "FALSE"  # random.choice([True, False])
		title = f"test task {str(num).zfill(3)}"
		urgency = random.randint(1, 5)
		importance = random.randint(1, 5)
		effort = random.randint(1, 3)
		due_date = ""  # default is no due date

		# Generate due date based on probability
		if random.random() < due_date_probability:
			time_between_dates = max_due_date - min_due_date
			random_number_of_days = random.randrange(time_between_dates.days)
			due_date = min_due_date + timedelta(days=random_number_of_days)
			if due_date > max_due_date:  # Ensure it's not after max_due_date
				due_date = max_due_date.strftime("%Y-%m-%d %H:%M:%S")
			due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")

		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		tasks.append([task_id, complete, title, urgency, importance, effort, due_date, now, now])

	return tasks


def main():
	tasks = generate_tasks(NUM_TASKS)
	with open(CSV_FILE, "w", newline="") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["id","complete","title","urgency","importance","effort","due_date","_created","_modified"])
		writer.writerows(tasks)
	print(f"{NUM_TASKS} tasks generated and saved to {CSV_FILE}")


if __name__ == "__main__":
	main()
