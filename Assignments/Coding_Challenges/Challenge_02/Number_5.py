# 5. User input 2

# Question:
# Using the following dictionary (or a similar one you found on the internet), 
# ask the user for a word, and compute the Scrabble word score for that word 
# (Scrabble is a word game, where players make words from letters, each letter is worth a point value), 
# steal this code from the internet, format it and make it work:
# letter_scores = {
#     "aeioulnrst": 1,
#     "dg": 2,
#     "bcmp": 3,
#     "fhvwy": 4,
#     "k": 5,
#     "jx": 8,
#     "qz": 10
# }

# Answer:
letter_scores = {'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,
                 'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,
                 'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}

def scrabble_word_count(word):
    count = 0
    for letter in word:
        count += letter_scores[letter]
    return count

word = input('Input scrabble word: ')
number = int(scrabble_word_count(word))
print('Your Score is: ',number)