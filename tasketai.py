"""
File name: tasketai.py
Description: Main runner file.

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

import inquirer
import src.task as task
from inquirer import errors
import src.user_data as user_data
from src.user_data import USER_TASK_FILE

MAX_TASKS_PER_PAGE = 20


def print_header():
	"""Prints the program header."""
	print("*" *  50)
	print(f"*{'Welcome to Tasketai!'.center(48, ' ')}*")
	print("*" * 50)


def task_input_validation(answers, current):
	"""
	Validates the task input.

	:param answers: The list of answers.
	:param current: The current answer.
	:raise: ValidationError
	"""
	title = answers.get("title", current)
	urgency = current if answers.get('title') else 1
	importance = current if answers.get('urgency') else 1
	effort = current if answers.get('importance') else 1
	try:
		assert task.is_valid_title(title), "Must be between 1 and 256 characters long"
		assert int(urgency) in range(1, 6), "Must be between 1 and 5"
		assert int(importance) in range(1, 6), "Must be between 1 and 5"
		assert int(effort) in range(1, 4), "Must be between 1 and 3"
	except AssertionError as err:
		raise errors.ValidationError("", reason=str(err))
	except KeyboardInterrupt:
		raise
	return True

def velocity_input_validation(answers, current):
	"""
	Validates the velocity input.

	:param answers: The list of answers.
	:param current: The current answer.
	:raise: ValidationError
	"""
	velocity = answers.get("velocity", current)
	try:
		assert int(velocity) in range(1, 4), "Must be between 1 and 3"
	except AssertionError as err:
		raise errors.ValidationError("", reason=str(err))
	except KeyboardInterrupt:
		raise
	return True


def view_task_list() -> None:
	"""Paginated view of task list."""
	task_df = task.load(USER_TASK_FILE)
	# print(f"[DEBUG] Loaded {len(task_df)} tasks")

	start = 0
	end = MAX_TASKS_PER_PAGE if len(task_df) > MAX_TASKS_PER_PAGE else -1
	load_more = True if len(task_df) > MAX_TASKS_PER_PAGE else False
	while True:
		task.display_list(task_df, start, end)
		if end >= len(task_df):
			load_more = False
		try:
			choice = inquirer.list_input("Select an option", choices=["See more", "Back"] if load_more else ["Back"])
			if choice == "Back":
				break
			elif choice == "See more":
				start = end
				end = start + MAX_TASKS_PER_PAGE

		except KeyboardInterrupt:
			break


def add_task_input() -> None:
	"""Prompts the user for the task to add."""
	try:
		questions = [
			inquirer.Text(f"title",
						  message=f"Title",
						  validate=task_input_validation),
			inquirer.Text("urgency",
						  message="Urgency",
						  validate=task_input_validation),
			inquirer.Text("importance",
						  message="Importance",
						  validate=task_input_validation),
			inquirer.Text("effort",
						  message="Effort",
						  validate=task_input_validation)
		]

		answers = inquirer.prompt(questions)
		if not answers:
			return
		task.add(title=answers.get('title'),
				 urgency=answers.get('urgency'),
				 importance=answers.get('importance'),
				 effort=answers.get('effort'),
				 csv_file=USER_TASK_FILE)

	except (TypeError, KeyboardInterrupt):
		return


def velocity_input() -> None:
	"""Prompts the user for their velocity."""
	choices = ["None (I have no wiggle room today)",
	           "Low (I have a lot on my plate, but I can fit something small in)",
	           "Medium (I can  definitely tackle a task or two)",
	           "High (My day is wide open!)",
	           "Back"
	           ]

	while True:
		try:
			choice = inquirer.list_input("Select your velocity for today",
			                             choices=choices
			                             )
			if choice == choices[-1]:
				break

			user_data.add_velocity(choice.index(choice))
			break

		except KeyboardInterrupt:
			break


def suggest_task_menu() -> None:
	"""Prompts the user to select suggested tasks."""
	pass


def main_menu():
	"""Provides the main menu."""
	user_data.greeting()
	while True:
		user_data.display()
		choices = []
		if not user_data.has_attr('velocity'):
			choices.append("Velocity")
		if not user_data.has_attr('selected_tasks'):
			choices.append("Suggest Tasks")

		try:
			choice = inquirer.list_input("Select an option",
										 choices= choices + [
											"Add Task",
											"View Task Backlog",
											"Quit"
											]
										 )
			if choice == "Quit":
				break
			elif choice == "Add Task":
				add_task_input()
			elif choice == "View Task Backlog":
				view_task_list()
			elif choice == "Velocity":
				velocity_input()
			elif choice == "Suggest Tasks":
				suggest_task_menu()

		except KeyboardInterrupt:
			break

	print("Goodbye!")


def main():
	print_header()
	# is_returning_today = dt.datetime.fromisoformat(data.get('last_login')).date() == dt.datetime.now().date()
	main_menu()

	# task_df = load_tasks_from_csv()
	# ranked_df = rank_tasks(task_df)
	# print_dataframe(ranked_df)


if __name__ == '__main__':
	main()
