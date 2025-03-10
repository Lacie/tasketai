"""
File name: rank_tasks.py
Description:

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

import pandas as pd
import datetime as dt
from datetime import datetime


def combine_relevance(urgency: int, importance: int) -> float:
    """
    Returns the combined relevance score for the given importance and urgency.

    This calculation weighs importance slightly more than urgency as to avoid the "urgency trap" commonly revealed in
    Eisenhower matrices.

    "Urgent but Not Important tasks are best described as busy work. These tasks are often based
    on expectations set by others and do not move you closer to your long-term goals."
    --https://www.todoist.com/productivity-methods/eisenhower-matrix

    For example, a task with an urgency of 1 and an importance of 4 would have a combined relevance of 4.8,
    whereas a task with an urgency of 4 and an importance of 1 would have a combined relevance of 3.8.

    :param urgency: The urgency level.
    :param importance: The importance level.
    :return: The combined relevance as a float, between 2.2 and 7.0.
    """
    if urgency >= 4 and importance >= 4:
        # Urgent and Important
        return 5 + (urgency / 5) + (importance / 5)
    elif urgency < 4 <= importance:
        # Not Urgent but Important
        return 4 + (importance / 5)
    elif urgency >= 4 > importance:
        # Urgent but Not Important
        return 3 + (urgency / 5)
    else:
        # Not Urgent and Not Important
        return 2 + ((urgency + importance) / 10)


def preprocess_tasks(task_dataframe: pd.DataFrame) -> pd.DataFrame:
    # Create features
    task_dataframe['combined_relevance'] = task_dataframe.apply(lambda r: combine_relevance(r['urgency'], r['importance']), axis=1)
    task_dataframe['has_due_date'] = task_dataframe['due_date'].notna().astype(int)
    task_dataframe['due_date'] = pd.to_datetime(task_dataframe['due_date'], errors='coerce')
    task_dataframe['days_until_due'] = (task_dataframe['due_date'] - dt.datetime.now()).dt.days
    task_dataframe['days_until_due'] = task_dataframe['days_until_due'].fillna(9999)  # df['days_until_due'].max()

    # Handle due date with multiplier
    task_dataframe['due_date_multiplier'] = 1.0
    if 'due_date' in task_dataframe.columns:
      task_dataframe['due_date'] = pd.to_datetime(task_dataframe['due_date'], errors='coerce')
      task_dataframe['days_until_due'] = (task_dataframe['due_date'] - datetime.now()).dt.days
      # Overdue tasks get a large boost that is weighed heavier the longer it's overdue
      task_dataframe.loc[task_dataframe['days_until_due'] < 0, 'due_date_multiplier'] = 1.5 + (abs(task_dataframe['days_until_due']) * 0.05)
      # Tasks due today get a medium boost
      task_dataframe.loc[task_dataframe['days_until_due'] == 0, 'due_date_multiplier'] = 1.5
      # Tasks due within a week get a smaller boost
      task_dataframe.loc[(task_dataframe['days_until_due'] > 0) & (task_dataframe['days_until_due'] < 7), 'due_date_multiplier'] = 1.25

      # Handle NAs, if any
      task_dataframe['days_until_due'] = task_dataframe['days_until_due'].fillna(9999)  # Fill with large number

    # Calculate the relevance score
    task_dataframe['relevance_score'] = task_dataframe['combined_relevance'] * task_dataframe['due_date_multiplier']

    return task_dataframe


def rank_tasks(task_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the given dataframe ranked according to multiple features.

    :param task_dataframe: The dataframe to rank.
    :return: A copy of the dataframe ranked in descending order.
    """
    incomplete_tasks = task_dataframe.loc[task_dataframe['complete'] == False]
    incomplete_tasks = preprocess_tasks(incomplete_tasks)
    ranked_tasks = incomplete_tasks.sort_values('relevance_score', ascending=False)
    ranked_tasks['rank'] = range(1, len(incomplete_tasks) + 1)

    return ranked_tasks


def print_dataframe(task_dataframe: pd.DataFrame, num_rows: int = None) -> None:
    # headers
    print(f"{'Rank'.ljust(4)}\t"
          f"{'Task'.ljust(32)}\t"
          f"{'Urgency'.ljust(8)}\t"
          f"{'Importance'.ljust(10)}\t"
          f"{'Effort'.ljust(10)}\t"
          f"{'Due Date'.ljust(18)}\t"
          f"{'Days Until Due'.ljust(14)}\t"
          f"{'Due Date Multiplier'.ljust(20)}\t"
          f"{'Combined Relevance'.ljust(18)}\t"
          f"{'Relevance Score'.ljust(16)}\t")

    # rows
    if num_rows:
        task_dataframe = task_dataframe[:num_rows]

    for index, row in task_dataframe.iterrows():
        print(f"#{str(row['rank']).zfill(3) if row['rank'] else '---'.ljust(4)}\t"
              f"{row['title'].rjust(32)}\t"
              f"{str(row['urgency']).ljust(8)}\t"
              f"{str(row['importance']).ljust(10)}\t"
              f"{str(row['effort']).ljust(10)}\t"
              f"{str(row['due_date']).ljust(18)}\t"
              f"{str(row['days_until_due']).ljust(14)}\t"
              f"{str(row['due_date_multiplier']).ljust(20)}\t"
              f"{str(row['combined_relevance']).ljust(18)}\t"
              f"{str(row['relevance_score']).ljust(16) if row['relevance_score'] else 'N/A'.ljust(16)}")
