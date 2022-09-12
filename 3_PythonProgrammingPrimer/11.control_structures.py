# Sequential
a = 1
b = 2
print(a)
print(b)

# Conditional
# if
a = 2
if a == 3:
    print("Found 3!")

if a == 2:
    print("Found 2!")

# if else
a = 7
if a % 2 == 0:
    print("even")
else:
    print("odd")

# if elif else
a = 4
if a == 1:
    print("do something")
elif a == 2:
    print("do something 2")
elif a == 3:
    print("")
else:
    print("else")

# Loops
# for
for i in range(5, 10):
    print(i)
# while
a = 1
while True:
    a += 1
    if a == 10:
        print("breaking while loop!")
        break

# comprehensions
# list
a = [1, 2, 3, 4, 5]
print([i ** 2 for i in a])
# dictionary
b = [6, 7, 8, 9, 10]
print({i: j for i, j in zip(a, b)})
