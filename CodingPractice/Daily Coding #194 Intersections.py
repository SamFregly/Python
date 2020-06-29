'''Suppose you are given two lists of n points, one list p1, p2, ..., pn on the
line y = 0 and the other list q1, q2, ..., qn on the line y = 1. Imagine a set
of n line segments connecting each point pi to qi. Write an algorithm to
determine how many pairs of the line segments intersect.'''


p_1 = [1, 2, 5, 3, 8,43,10, 4]
p_2 = [-2,4,-2, 0, 3,36, 5,-1]

def loop(points,matches) :
    a = points[0]
    #print(matches)
    if len(points) == 1:
        #print(matches, '###')
        q = matches
        return q
    for i in points[1:]:
        #print(a[0], i[0])
        if (a[0] < i[0] and a[1] > i[1]) or (a[0] > i[0] and a[1] < i[1]):
            #print(a,i)
            x = (a,i)
            matches.add(x)
            #print(matches)
    return loop(points[1:],matches)



match = set()
def is_intersect(p1,p2,match):
    p3 = []

    for i,v in enumerate(p1):
        x = v,p2[i]
        #print(x)
        p3.append(x)
    #print(p3)
    return loop(p3,match)
    #return crosses




x = is_intersect(p_1,p_2,match)
print(match)
print(x)
