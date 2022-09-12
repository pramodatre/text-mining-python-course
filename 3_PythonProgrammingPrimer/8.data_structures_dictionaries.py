# Dictionary characteristics
a = {}
b = {1: 2, 2: 3, 3: 4}
print(a)
print(b)

# Adding items to a dictionary
a["a"] = 1
a["b"] = 2
print(a)

# Update a dictionary
b.update(a)
print(b)

# Accessing items
print(b[1])
print(b["a"])

# Check if a key is present
print(1 in b)
print(7 in b)

# Remove a key
del b["a"]
print(b)
