class Thing:
  def __init__(self):
    self.stuff = []

  def __repr__(self):
    return "<Thing stuff=%s>" % (self.stuff, )

x = Thing() #a thing is created which is an instance of class 'Thing'
# it's a child that points at its parent
# the word 'x' is now a reference to that thing which was created
x.stuff = ["Pony"] #create a new array that has pony in it
# first a string is created
# then an array and that string 'Pony' is put into the array
# change x's stuff reference to the array that has 'Pony' in it
y = Thing() #another thing that is created which is an instance of class 'Thing'
y.stuff = x.stuff #sets y's stuff reference to point at the same as x's stuff reference
# in Python, all values are objects
# 'A pointer refers to a place in memory'
y.stuff.append("Horse")
#'y' ---> a thing of Thing
#'y.stuff' ----> y ---> stuff
# In this case, 'y.stuff' ---> y ---> stuff ---> a list
#'y.stuff.append' ---> y ---> stuff ----> append --> a function
# Python documentation: 'append() adds an item to the end of the list'
print(y) #['Pony', 'Horse']
print(x) #['Pony', 'Horse']


#a: pointing at the value at the same memory allocation

# An object is a combination of state and behaviour
# In this case, two objects share the same state.

x.stuff = ['Cow']
# create a new array that has Cow in it
# first a string is created
# then an array and that string 'Cow' is put into the array
# change x's stuff reference to the array that has 'Cow' in it
print(x)
print(y)
