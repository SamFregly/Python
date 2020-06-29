'''Given an array of elements, return the length of the longest subarray where
all its elements are distinct.

For example, given the array [5, 1, 3, 5, 2, 3, 4, 1], return 5 as the longest
subarray of distinct elements is [5, 2, 3, 4, 1].'''
from pprint import pprint

x = [5, 1, 3, 5, 2, 3, 4, 1,3,6,7,2,4,67,3,2,2,7,6,5,4,3,21,0,9,8,7]
temp = []
max = 0

def longest(x,max):
    temp = []
    best = []
    for i in x:
        if i not in temp:
            temp.append(i)
        else:
            max = len(temp) if len(temp) > max else max
            best = temp
            temp = [i]
    return best


a = longest(x,max)
pprint(a)
print(a)
