## RECAP Read&Write.py

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder
# Just a function, never mind it just returns a path
from __init__ import example_path

# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()

# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: Variables")))

# We can set or create variables using the 'set_variable' method. 
# Parameters:
#     var: the name of the variable
#     value: the value of the variable; supported data types are string, integer, float, boolean, tuple, list, and dict
#     mode (default: 'w'): if the mode is 'w', it overwrites or creates the variable. If it is 'x', it creates the variable if it does not exist, and does not modify it if it exists
#     runtime (default: False): if the runtime is True it does not write the variable to the HDSIo
#     file: Don't mind it for now; we will learn about them later.
hds.set_variable("x","1","w",False,"main")

# Example:
name = input("Your Name: ")
age = input("Age: ")
about_hds = input("About HDS: ")
hds.set_variable("name",name)
hds.set_variable("age",age)
hds.set_variable("about_hds",about_hds)

# Saving
hds.save()

# Create another instance of the HyperDataStorage class.
hds = HyperDataStorage()

# Reading it again to refresh the changes.
hds.read(HDSFolder(example_path("Lesson: Variables")))

# We can use the 'iter_var' method to get a dictionary containing only the variables and values
# Parameters:
#     file: Don't mind it for now; we will learn about them later.
print("Printing variables and values:")
for key,value in hds.iter_vars().items():
    print(key,value,sep=": ")

# Getting a specific variable
var = input("Variable to retrieve: ")
print("Retrieved value: "+hds.get_variable(var))
# OR
# hds.variables["main"][var][0] to get the variable from the main.hds

# You can also delete a variable by using the 'delete_variable' method
hds.delete_variable(var)