table = []
n =10
A=12
c = 0
for i in range(0,n):
    new = []
    for j in range(0,n):
        q = (j+1)*(i+1)
        if q == A:
            c+=1
        new.append(q)
    print(new)
    table.append(new)

print(table)
print(c)
