"""
File name: tasketai.py
Description: Main runner file.

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

import inquirer
import src.task as task
from inquirer import errors
import src.user_data as user_data
from src.user_data import USER_TASK_FILE

MAX_TASKS_PER_PAGE = 20
MAX_SUGGESTIONS_PER_PAGE = 3
EFFORT_DICT = {1: "LOW", 2: "MED", 3: "HIGH"}


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
						  validate=task_input_validation),  # lambda _, x: 1 <= len(x) <= 256),
			inquirer.Text("urgency",
						  message="Urgency",
						  validate=task_input_validation),  # lambda _, x: 1 <= x <= 5),
			inquirer.Text("importance",
						  message="Importance",
						  validate=task_input_validation),  # lambda _, x: 1 <= x <= 5),
			inquirer.Text("effort",
						  message="Effort",
						  validate=task_input_validation),  # lambda _, x: 1 <= x <= 3)
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
	choices = [("None (I have no wiggle room today)", 0),
	           ("Low (I have a lot on my plate, but I can fit something small in)", 1),
	           ("Medium (I can  definitely tackle a task or two)", 2),
	           ("High (My day is wide open!)", 3),
	           ("Back", -1)]

	try:
		choice = inquirer.list_input("Select your velocity for today", choices=choices)
		if choice == -1:
			return
		user_data.add_velocity(choice)

	except KeyboardInterrupt:
		return


def settings_menu() -> None:
	"""Opens the settings menu."""
	choices = [("Change username", 1),
	           ("Back", -1)]

	try:
		choice = inquirer.list_input("Select your velocity for today", choices=choices)
		if choice == -1:
			return
		if choice == 1:
			username = inquirer.text(message="Enter new username")
			user_data.add_username(username)

	except KeyboardInterrupt:
		return

def merge_task_suggestions(task_list_1, task_list_2, n: int = 4) -> list:
	"""Prompts the user to merge task suggestions."""
	"""
	Merges task_list_2 into task_list_1 at every nth and nth + 1 index.
	Example 1:
		task_list_1 = [0, 1, 2, 3, 4]
		task_list_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		index = 4
		result = [0, 1, 2, 3, 'a', 'b', 4, 'c', 'd', 'e', 'f', 'g']
	Example 2:
		task_list_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
		task_list_2 = ['a', 'b', 'c']
		index = 4
		result = [0, 1, 2, 3, 'a', 'b', 4, 5, 6, 7, 'c', 8, 9, 10, 11, 12]
	
	:param task_list_1: The list to be merged into.
	:param task_list_2: The list to merge.
	:param n: The nth index of the list to be merged.
	"""
	insert_count = 0
	for i in range(len(task_list_1)):
		if i > 0 and i % n == 0:
			# get chunks of length 2 from list 2
			task_list_2_chunk = [task_list_2.pop(0), task_list_2.pop(0)] if len(task_list_2) >= 2 else [task_list_2.pop(0)] if len(task_list_2) >= 1 else []
			# insert at nth index
			task_list_1.insert(i + insert_count, task_list_2_chunk)
			# keep track of inserts to offset index shift from insertion
			insert_count += 1

	task_list_1.extend(task_list_2)  # Add any leftovers
	task_list_1 = [element for item in task_list_1 for element in (item if isinstance(item, list) else [item])]  # flatten the list

	return task_list_1


def get_suggestions(velocity: int):
	"""
	Prompts the user to select from a paginated view of suggested tasks.

	:param velocity: The velocity of the user.
	"""
	task_file = user_data.get_attr('task_csv')
	ranked_tasks = task.rank(task_file)
	selected_tasks = user_data.get_attr('selected_tasks') if user_data.get_attr('selected_tasks') else []

	suggested_task_ids = []
	if velocity == 1:
		low_effort_tasks = ranked_tasks.loc[ranked_tasks['effort'] == 1]
		for index, row in low_effort_tasks.iterrows():
			suggested_task_ids.append(row['id']) if row['id'] not in selected_tasks else None

	elif velocity == 2:
		low_effort_tasks = ranked_tasks.loc[ranked_tasks['effort'] == 1]
		medium_effort_tasks = ranked_tasks.loc[ranked_tasks['effort'] == 2]

		for index, row in medium_effort_tasks.iterrows():
			suggested_task_ids.append(row['id']) if row['id'] not in selected_tasks else None

		low_effort_task_ids = []
		for index, row in low_effort_tasks.iterrows():
			low_effort_task_ids.append(row['id']) if row['id'] not in selected_tasks else None
		suggested_task_ids = merge_task_suggestions(suggested_task_ids, low_effort_task_ids)

	elif velocity == 3:
		pass

	return ranked_tasks.loc[ranked_tasks['id'].isin(suggested_task_ids)]


def suggest_task_menu() -> None:
	"""Prompts the user to select suggested tasks."""
	velocity = user_data.get_attr('velocity') - user_data.get_selected_effort()
	suggested_tasks = get_suggestions(velocity)

	start_index = 0
	end_index = MAX_SUGGESTIONS_PER_PAGE if len(suggested_tasks) > MAX_SUGGESTIONS_PER_PAGE else -1
	load_more = True if len(suggested_tasks) > MAX_SUGGESTIONS_PER_PAGE else False
	remaining_velocity = velocity
	selected_tasks = set()

	try:
		while remaining_velocity > 0:
			suggested_tasks = get_suggestions(remaining_velocity)

			if end_index >= len(suggested_tasks):
				load_more = False

			current_choices = []

			for index, row in suggested_tasks[start_index:end_index].iterrows():
				current_choices.append((f"[{EFFORT_DICT.get(row['effort'])}] {row['title']}", str(row['id'])))
				user_data.add_task("suggested", str(row['id']))

			current_choices.append(('See more', 0)) if load_more else None
			current_choices.append(('Back', -1))

			choice = inquirer.list_input("Select a task", choices=current_choices)

			if choice == -1:
				break

			elif choice == 0:
				start_index = end_index
				end_index = start_index + MAX_SUGGESTIONS_PER_PAGE
				continue

			else:
				effort = list(suggested_tasks.loc[suggested_tasks['id'] == choice].get('effort'))[0]
				selected_tasks.add(choice)
				remaining_velocity -= effort

			for selected_task in selected_tasks:
				user_data.add_task("selected", selected_task)


	except KeyboardInterrupt:
		return


def main_menu():
	"""Provides the main menu."""
	user_data.greeting()
	while True:
		user_data.display_message()
		choices = []
		if not user_data.has_attr('velocity'):
			choices.append(("Velocity", 3))
		if user_data.has_attr('velocity') and (not user_data.has_attr('selected_tasks') or user_data.get_selected_effort() < user_data.get_attr('velocity')):
			choices.append(("Suggest Tasks", 4))

		try:
			choice = inquirer.list_input("Select an option",
										 choices= choices + [
											("Add Task", 1),
											("View Task Backlog", 2),
											("Settings", 0),
											("Quit", -1)
											]
										 )
			if choice == -1:
				break
			elif choice == 1:
				add_task_input()
			elif choice == 2:
				view_task_list()
			elif choice == 3:
				velocity_input()
			elif choice == 4:
				suggest_task_menu()
			elif choice == 0:
				settings_menu()

		except KeyboardInterrupt:
			break

	print("Goodbye!")


def main():
	print_header()
	main_menu()


if __name__ == '__main__':
	main()
