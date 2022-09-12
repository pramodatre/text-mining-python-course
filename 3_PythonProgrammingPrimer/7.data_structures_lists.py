# List characteristics
a = []
b = [1, 2, 3, 4]
c = ["a", 2, 4.5]
print(a)
print(b)
print(c)

# Adding items to a list
# append
a.append(2)
print(a)

# extend
b.extend(a)
print(b)
# Accessing items in a list
# index
print(b[2])

# Removing items from a list
# remove
b.remove(3)
print(b)
b.remove(2)
print(b)
# pop
item = b.pop()
print(b)
item = b.pop(0)
print(item)
print(b)

# Check for an item in a list
print(2 in c)
print(5 in c)

# Concatenate lists
f = [4, 5, 6]
c += f
print(c)
