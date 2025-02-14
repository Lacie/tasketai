# tasketai

---

## Installation

Install dependencies with the following command
```
pip install -r requirements.txt
```

---

## Usage

Run the program with the following command
```
python tasketai.py
```

Running the program will display the [Main Menu](#main-menu). The options that are displayed depend on the user's current state.

![tasketai_main-menu](../images/tasketai_main-menu.png)

## Navigation

- Navigate menus using the `↑`/`↓` arrow keys.
- Select a highlighted option by pressing `⏎`/`Enter`.
- Return to a previous menu with `Ctrl + C` or by selecting `Back` from a sub-menu.
- Cancel an input prompt with `Ctrl + C`.
- Exit the program using `Ctrl + C` or by selecting `Quit` from the main menu.

_Thank you to the [inquirer](https://pypi.org/project/inquirer/) Python module for offering these beautiful and easy-to-use menus!_

---

## Options

### Main Menu

There are several static options in the main menu that are always available. These options are:
- [Add Task](#add-task)
- [View Task Backlog](#view-task-backlog)
- [Settings](#settings)
- Quit

The following options will display only under certain circumstances:
- [Velocity](#velocity)
- [Suggest Tasks](#suggest-tasks)

### Velocity

The Velocity option will be available if you have not yet entered your velocity for the day.

![tasketai_velocity](../images/tasketai_velocity.png)

### Suggest Tasks

The Suggest Tasks option will only be available if you have entered your velocity for the day AND the combined effort of your selected tasks is lower than your velocity.

![tasketai_suggest-task--none-selected](../images/tasketai_suggest-task--none-selected.png)

For example, if you have entered a HIGH velocity, but have only selected a single task of LOW effort, the Suggest Task option will still be available.

![tasketai_suggest-task--under-velocity](../images/tasketai_suggest-task--under-velocity.png)

You will not be able to select more tasks than your entered velocity. If your selected tasks equal your velocity, the Suggest Task option will no longer be available.

![tasketai_suggest-task--at-velocity](../images/tasketai_suggest-task--at-velocity.png)

### Add Task

Select this option to add a task to your backlog.

You will be prompted for the following input:
- `Title` The name or title of the task. Must be between 1 and 256 characters.
- `Urgency` How urgent the task is on a scale of 1-5, with 1 being not urgent and 5 being very urgent.
- `Importance` How important the task is on a scale of 1-5, with 1 being not important and 5 bein very important.
- `Effort` How much effort the task will take to complete on a scale of 1-3, with 1 being low effort and 3 being high effort.

Values for all 4 inputs are required to successfully save the task. Cancelling with Ctrl+C before the task is saved will discard any current input and return you to the main menu.

![tasketai_add-task](../images/tasketai_add-task.png)

### View Task Backlog

Displays a paginated view of your current task backlog by order of when they were added. The maximum number of tasks displayed per page is 20.
The "See more" option is available if you have more tasks to view.

![tasketai_view-task-backlog](../images/tasketai_view-task-backlog.png)

### Settings

Select this option to view and update user settings.

![tasketai_settings-menu](../images/tasketai_settings-menu.png)

#### Update Username

Select this option to add or update your username.

To delete your current username, leave the input field blank.

![tasketai_update-username](../images/tasketai_update-username.png)

---
