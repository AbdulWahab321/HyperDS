# RECAP Read&Write.py

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder
# Just a function, never mind it just returns a path
from __init__ import example_path
import pickle
serializer_module = pickle  # You can use any serializer module used for serializing objects to file 
# Create an instance of the HyperDataStorage class with serializer module arg
# What is a serializer module?
"""
a serializer module is responsible for converting an object in memory into a stream of bytes that can be saved to a file, sent over a network, or otherwise persisted or transmitted. This process is called serialization.
Python has several built-in serialization modules, including pickle, dill.
pickle is a module that can be used to serialize and deserialize Python objects. It can serialize most Python objects, including custom classes, and can preserve the object's state (i.e., instance variables).
"""
hds = HyperDataStorage(serializer_module)

# Creating a class
class Test():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self):
        return self.x + self.y
    def subtract(self):
        return self.x - self.y
test = Test(100,50)

# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: Python Objects")))

########################################################################################################
## WARNING: The object ('Test' in this condition) should be created before calling the 'read' method ##
########################################################################################################

# We can set or create variables using the 'add_python_obj' method
# Parameters are similar to 'set_variable' method except the var is changed to name and value changed to obj
hds.add_python_obj("math",test)

# Saving 
hds.save()

# Create another instance of the HyperDataStorage class.
hds = HyperDataStorage()

# Reading it again to refresh the changes.
hds.read(HDSFolder(example_path("Lesson: Python Objects")))

# Getting the python object test from hds
math = hds.get_python_obj("math")
print(math.add()) 
### You should get the output 150
print(math.subtract())
### You should get the output 50