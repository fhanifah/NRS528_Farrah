# 2. List overlap

# Question:
# Using these lists:
# list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
# list_b = ['dog', 'hamster', 'snake']
# 1. Determine which items are present in both lists.
# 2. Determine which items do not overlap in the lists.


# Answer:
A = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
B = ['dog', 'hamster', 'snake']

# 1. Determine which items are present in both lists
C = []
for animal in A:
    if animal in B:
        C.append(animal)
print('Items are present in both list_a and list_b: ',C)

# 2. Determine which items do not overlap in the lists
D=[]
for animal in A:
    if animal not in B:
        D.append(animal)
for animal in B:
    if animal not in A:
        D.append(animal)
print('Items do not overlap in both list_a and list_b: ',D)