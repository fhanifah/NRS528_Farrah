# 1. Simple directory tree

# Question:
# Replicate this tree of directories and subdirectories:

# ├── draft_code
# |   ├── pending
# |   └── complete
# ├── includes
# ├── layouts
# |   ├── default
# |   └── post
# |       └── posted
# └── site

# 1. Using os.system or os.mkdirs replicate this simple directory tree.
# 2. Delete the directory tree without deleting your entire hard drive.

# Answer:
import os

# 1. Using os.system or os.mkdirs replicate this simple directory tree
os.mkdir('draft_code')
os.mkdir('draft_code/pending')
os.mkdir('draft_code/complete')
os.mkdir('includes')
os.mkdir('layouts')
os.mkdir('layouts/default')
os.mkdir('layouts/post')
os.mkdir('layouts/post/posted')
os.mkdir('site')

# list directory tree
print('List of main directory tree:',os.listdir('.'))
print('List of draft_code directory:',os.listdir('draft_code'))
print('List of layouts directory:',os.listdir('layouts'))
print('List of post directory inside layouts directory:',os.listdir('layouts/post'))

# 2. Delete the directory tree without deleting your entire hard drive.
os.removedirs('draft_code/pending')
os.removedirs('draft_code/complete')
os.removedirs('includes')
os.removedirs('layouts/post/posted')
os.removedirs('layouts/default')
os.removedirs('site')