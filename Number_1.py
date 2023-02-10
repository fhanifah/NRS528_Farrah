# 1. List Values

# Question:
# Using list: [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
# You need to do two separate things here and report both in your Python file. 
# You should have two solutions in this file, one for item 1 and one for item 2. 
# Item 2 is tricky so if you get stuck try your best (no penalty), for a hint check out the solution by desiato.

# 1. Make a new list that has all the elements less than 5 from this list in it and print out this new list.
# 2. Write this in one line of Python (you do not need to append to a list just print the output).


# Answer:
list = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]

# 1. Make a new list that has all the elements less than 5 from this list in it and print out this new list. 
new_list = []
for item in list:
    if item < 5:
        new_list.append(item) 
print('List 1 = ', new_list)

# 2. Write this in one line of Python
print('List 2 = ',[(it) for it in list if it < 5])