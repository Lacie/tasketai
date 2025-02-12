"""
File name: tasketai.py
Description: Main runner file.

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

from src.rank_tasks import rank_tasks, print_dataframe
from src.task import load_tasks_from_csv

def get_daily_velocity() -> int:
	pass


def main():
	task_df = load_tasks_from_csv()
	ranked_df = rank_tasks(task_df)

	print_dataframe(ranked_df)



if __name__ == '__main__':
	main()
