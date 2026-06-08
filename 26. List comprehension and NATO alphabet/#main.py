import random

# List comprehension
# numbers = [1, 2, 3]
# new_list = [n + 1 for n in numbers]
# print(new_list)

# new_list = [n * 2 for n in range(1, 5)]
# print(new_list)

# # Conditional list comprehension
# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
# short_names = [name for name in names if len(name) < 5]
# print(short_names)
# long_names = [name.upper() for name in names if len(name) > 5]
# print(long_names)

# # Dictionary comprehension
# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
# student_scores = {student: random.randint(1, 100) for student in names}
# passed_students = {
#     student: score for (student, score) in student_scores.items() if score >= 60
# }
# print(passed_students)

# How to iterate over a pandas DataFrame
# import pandas

# student_dict = {
#     "student": ["Angela", "James", "Lily"],
#     "score": [56, 76, 98]
# }

# student_data_frame = pandas.DataFrame(student_dict)
# # print(student_data_frame)

# for (index, row) in student_data_frame.iterrows():
#     print(row)