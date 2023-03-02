## RECAP Read&Write.py

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder
# Just a function, never mind it just returns a path
from __init__ import example_path

# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()

# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: Multiple Files")))

# What if you need to have multiple files in your HDSIo?
# Lets add a file called "additionalfile.txt" with the contents "I'm an addtional file"

# For that we can use the 'add_file' method 
hds.add_file("additionalfile.txt","I'm an addtional file")
hds.save()

# Now we can see a file called "additionalfile.txt" in the folder: "Lesson: Multiple Files"
# Now let's open that file and make changes

hds = HyperDataStorage()
hds.read(HDSFolder(example_path("Lesson: Multiple Files")))

# For opening file with method 'open_file' with modes 'rb', 'wb', 'r' or 'w'   we can use the open_file method
additional_file = hds.open_file("additionalfile.txt","w")
# Now let's write some other stuff
additional_file.write("You changed me!")

# What if you want to add a file as hds and set variables in it?
# We can do it using the add_file method but leaving the parameter data as None:
# The filename should end with .hds
hds.add_file("test.hds") 
# Now let's set variables in the test.hds

# RECAP Variables.py
# We need to set the variable in test.hds, So we will pass file="test" (.hds should not be added) to the set_variable
# All methods supports file argument (eg. set_variable,get_variable,iter_vars,add_python_obj,get_python_obj etc)
hds.set_variable("How_is_HDS","Awesome",file="test")

# Now let's retrieve the variable
how_is_hds = hds.get_variable("How_is_HDS",file="test")
print(how_is_hds)

# What if we need to import all the variables from test.hds to main.hds?
# We will use the 'add_import' method for it
# Parameters:
#     import_filename: file we need to import (test in this case)
#     file: which file we need to import to (main in this case)
hds.add_import("test","main")

# Now let's test if How_is_HDS variable is available in main.hds 

hds.save()

hds = HyperDataStorage()
hds.read(HDSFolder(example_path("Lesson: Multiple Files")))
print(hds.get_variable("How_is_HDS",file="main"))
## You should see the output as Awesome!