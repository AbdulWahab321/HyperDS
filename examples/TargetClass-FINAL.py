## RECAP EVERYTHING

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder, HDSObject
# Just a function, never mind it just returns a path
from __init__ import example_path
import datetime

# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()
# Creating a target class (Saves all the variables,python objects, etc)
target_class = hds.new_target_class()

class SomeClass:
    def __init__(self):
        pass
someclass = SomeClass()
# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: TargetClass & FINAL")),target_class=target_class,allow_pyevals=False)

hds.set_variable("greeting_msg","Greeetinggg")
hds.add_python_obj("mycls",someclass)

obj = HDSObject("Me")
obj.add_var("name","hyperDS")
obj.add_var("description","Powerfull data storage!")
obj = obj.add_obj("Data")
obj.add_var("date",str(datetime.datetime.now()))

hds.add_obj(obj)

hds.add_file("test.hds")
hds.set_variable("name","test",file="test")

someclass = hds.get_python_obj("mycls")

hds.set_pyeval("hi","print('Hi')",file="main")

# We are using devlogs=True to know what all are happening while reading each file
hds.save(devlogs=True)


# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()
# Creating a target class (Saves all the variables,python objects, etc)
target_class = hds.new_target_class()

# We're using HDSFolder to make it easier to manually read the file.
hds.read(HDSFolder(example_path("Lesson: TargetClass & FINAL")),target_class=target_class)

# Listing all hds files
print(dir(target_class))
print("")
# Listing all the variables, python objects etc in main.hds
print(dir(target_class.main))
print("")
# Listing all the variables, python objects etc in test.hds
print(dir(target_class.test))