# 4. User input

# Question:
# Ask the user for an input of their current age, and tell them how many years until they reach retirement (65 years old).
# Hint:
# age = input("What is your age? ")
# print "Your age is " + str(age)

# Answer:
age = int(input('What is your age? '))
age_retirement = 65
year_left = age_retirement - age
print('Your age is ' + str(age) + ' years old')
print(str(year_left) + ' years left until you reach retirement (65 years old)')