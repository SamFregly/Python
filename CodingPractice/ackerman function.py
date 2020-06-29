import resources, sys
#resources.setrlimit(resources.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)
import timeit
import time
start_time = time.time()

def A(m, n, s ="% s"): 
    #print(s % ("A(% d, % d)" % (m, n))) 
    if m == 0: 
        return n + 1
    if n == 0: 
        return A(m - 1, 1, s) 
    n2 = A(m, n - 1, s % ("A(% d, %% s)" % (m - 1))) 
    return A(m - 1, n2, s) 
  
print(A(3, 9))
print("--- %s seconds ---" % (time.time() - start_time))

#print(timeit.timeit(A(3, 3), number=1))
