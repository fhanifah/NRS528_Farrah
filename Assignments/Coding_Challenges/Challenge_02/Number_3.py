# 3. Given a singe phrase, count the occurrence of each word

# Question:
# Using this string:
# string = 'hi dee hi how are you mr dee'
# Count the occurrence of each word, and print the word plus the count 
# (hint, you might want to "split" this into a list by a white space: " ").


# Answer:
string = ['hi', 'dee', 'hi', 'how', 'are', 'you', 'mr', 'dee']

# 1st method using loop and count
print('1st method using loop and count:')
for word in string:
    print(word,':',string.count(word))

# 2nd method using pandas and numpy
import pandas as pd
import numpy as np
print('2nd method using pandas and numpy:')
print(pd.value_counts(np.array(string)))