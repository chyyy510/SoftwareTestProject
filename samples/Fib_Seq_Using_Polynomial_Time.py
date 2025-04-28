def fib(n):
    c = 0
    p = 1
    g = 0

    if n == 0 or n == 1:
        return n
        
    for i in range(n-1):
        c = p + g
        p, g = c, p
    return c
