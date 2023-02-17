# 2. Push sys.argv to the limit

# Question:
# Construct a rudimentary Python script that takes a series of inputs as a command from a bat file using sys.argv, and does something to them. The rules:

# 1. Minimum of three arguments to be used.
# 2. You must do something simple in 15 lines or less within the Python file.
# 3. Print or file generated output should be produced.

# Answer:
import sys

argument_list = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])]
counter = 1

for i in argument_list:
    if i/4 - int(i/4) == 0:
        print('Year',i,'is a leap year')
    else:
        print('Year',i,'is not a leap year')

