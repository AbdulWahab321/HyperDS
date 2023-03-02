## RECAP Read&Write.py

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder, HDSObject
# Just a function, never mind it just returns a path
from __init__ import example_path

# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()

# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: HDSObjects")))

# What if we need to have objects like classes in HyperDataStorage (Supports only variables)
# An example will be the following:

# Creating a class with a variable:
theobj = HDSObject("ME")
theobj.add_var("name","My name!")
theobj.add_var("age","17")

# Now you can see a class ME with name in Lesson: HDSObjects/main.hds
# What if you want to create an object inside this object eg. About School
# Let's add a object called school

theobj = theobj.add_obj("School")
theobj.add_var("Name","GMVHSS")  
theobj.add_var("Address","Place") 
# You can add as many objects like this
# for example you can add AboutSchool class by using theobj = theobj.add_obj("AboutSchool")

# Now let's add the object
hds.add_obj(theobj) 
hds.save()