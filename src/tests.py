from tasketai import merge_task_suggestions


def test_merge_task_suggestions():
	list_1 = list(range(20))
	list_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	merged_list = merge_task_suggestions(list_1, list_2)
	expected = [0, 1, 2, 3, 'a', 'b', 4, 5, 6, 7, 'c', 'd', 8, 9, 10, 11, 'e', 'f', 12, 13, 14, 15, 'g', 16, 17, 18, 19]
	assert merged_list == expected, f"Test case 1 failed. Got: {merged_list}, Expected: {expected}"

	list_1 = list(range(5))
	list_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	merged_list = merge_task_suggestions(list_1, list_2)
	expected = [0, 1, 2, 3, 'a', 'b', 4, 'c', 'd', 'e', 'f', 'g']
	assert merged_list == expected, f"Test case 2 failed. Got: {merged_list}, Expected: {expected}"

	list_1 = list(range(10))
	list_2 = ['a', 'b']
	merged_list = merge_task_suggestions(list_1, list_2)
	expected = [0, 1, 2, 3, 'a', 'b', 4, 5, 6, 7, 8, 9]
	assert merged_list == expected, f"Test case 3 failed. Got: {merged_list}, Expected: {expected}"

	list_1 = list(range(10))
	list_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	merged_list = merge_task_suggestions(list_1, list_2, chunk_size=3, nth_index=2)
	expected = [0, 1, 'a', 'b', 'c', 2, 3, 'd', 'e', 'f', 4, 5, 'g', 6, 7, 8, 9]
	assert merged_list == expected, f"Test case 3 failed. Got: {merged_list}, Expected: {expected}"

	return True

try:
	test_merge_task_suggestions()
	print("merge_task_suggestions() tests passed")
except AssertionError as err:
	print(err)
