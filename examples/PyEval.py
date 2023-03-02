## RECAP Read&Write.py

# Import the required classes from the hyperDS module.
from hyperDS import HyperDataStorage, HDSFolder, HDSObject
# Just a function, never mind it just returns a path
from __init__ import example_path

# Create an instance of the HyperDataStorage class.
hds = HyperDataStorage()

# We're using HDSFolder to make it easier to manually read the file.
# We are disabling pyevals for now
hds.read(HDSFolder(example_path("Lesson: PyEval")),allow_pyevals=False)

# Let's create a pyeval code which prints HI
hds.set_pyeval("hi","print('HI')")
# Now when we run the code twice (first will save and the second third etc will run) we should see HI in the terminal

# What if we need to run the code with some variables or function
# For example we created a function for greeting and we need to call it inside pyeval
# Let's create a function for greeting
def greet(name):
    print("Hi, "+name)
# To call the greet inside pyeval we need to pass eval_kwargs parameter to read function like this:
hds.read(HDSFolder(example_path("Lesson: PyEval")),eval_kwargs={"greet":greet})
hds.set_pyeval("greets","greet('HyperDS')")
# Now we should see the HI HyperDS

# What if we need to export a variable to hds from pyeval?
# For example we will compute an area of a rectangle and add it to the hds variables
# We can do it like this:
hds.set_pyeval("script","""
lenght = 10
breadth = 20
area = lenght*breadth

# To add the variable 'area' to the hds variables we need to use the method export?
# This adds the variable 'area' to the variables of the file where the script called 
export("area",area,"variables")

# What if we need to export the variable 'area' to the hds variables of some other file?
# For that we need to 'export_to' method:
export_to("area",area,"variables",file="main")

# What if we need to add the variable 'area' to the file?
export_to("area",area,"variables",file="main",runtime=False)


# What if we need to add a object to hds?              
class Test():
    pass
test = Test()
# Unfortunately export doesn't support to add class to the file yet.
export("test",test,"python_object")

""")
hds.save()