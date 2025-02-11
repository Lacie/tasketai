"""
File name: rank_tasks.py
Description:

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

import pandas as pd
from pathlib import Path
from datetime import datetime

CSV_FILE = Path("./data/generated-test-tasks.csv")


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


def rank_tasks(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the given dataframe ranked according to multiple features.

    :param dataframe: The dataframe to rank.
    :return: The ranked dataframe.
    """
    # Handle due date with multiplier
    dataframe['due_date_multiplier'] = 1.0
    if 'due_date' in dataframe.columns:
      dataframe['due_date'] = pd.to_datetime(dataframe['due_date'], errors='coerce')
      dataframe['days_until_due'] = (dataframe['due_date'] - datetime.now()).dt.days
      # Overdue tasks get a large boost that is weighed heavier the longer it's overdue
      dataframe.loc[dataframe['days_until_due'] < 0, 'due_date_multiplier'] = 1.5 + (abs(dataframe['days_until_due']) * 0.05)
      # Tasks due today get a medium boost
      dataframe.loc[dataframe['days_until_due'] == 0, 'due_date_multiplier'] = 1.5
      # Tasks due within a week get a smaller boost
      dataframe.loc[(dataframe['days_until_due'] > 0) & (dataframe['days_until_due'] < 7), 'due_date_multiplier'] = 1.25

      # Handle NAs, if any
      dataframe['days_until_due'] = dataframe['days_until_due'].fillna(9999)

    dataframe['relevance_score'] = dataframe['combined_relevance'] * dataframe['due_date_multiplier']
    ranked_tasks = dataframe.sort_values('relevance_score', ascending=False)
    return ranked_tasks

# Load data
test_df = pd.read_csv(CSV_FILE)
# TODO drop completed tasks

# Create features
test_df['combined_relevance'] = test_df.apply(lambda r: combine_relevance(r['urgency'], r['importance']), axis=1)
test_df['has_due_date'] = test_df['due_date'].notna().astype(int)
test_df['due_date'] = pd.to_datetime(test_df['due_date'], errors='coerce')
test_df['days_until_due'] = (test_df['due_date'] - datetime.now()).dt.days
test_df['days_until_due'] = test_df['days_until_due'].fillna(9999)  # df['days_until_due'].max()

# Rank 'em
ranked_df = rank_tasks(test_df.copy())
ranked_df['rank'] = range(1, len(ranked_df) + 1)

# Print ranked tasks
for index, row in ranked_df.iterrows():
    print(f"#{str(row['rank']).zfill(3)} --> {row['title'].rjust(32)}\t"
          f"Urgency: {row['urgency']}\t"
          f"Importance: {row['importance']}\t"
          f"Due Date: {str(row['due_date']).ljust(18)}\t"
          f"Days Until Due: {str(row['days_until_due']).ljust(5)}\t"
          f"Due Date Multiplier: {row['due_date_multiplier']}\t"
          f"Combined Relevance: {row['combined_relevance']}\t"
          f"Relevance Score: {row['relevance_score']}")
