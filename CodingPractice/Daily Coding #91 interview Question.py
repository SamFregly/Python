functions = []

for i in range(10):
    a = []
   # print(i)
    functions.append(lambda : i)
    for f in functions:
       a.append((f(),f))
    print(a,i)
    

for f in functions:
    print(f())
