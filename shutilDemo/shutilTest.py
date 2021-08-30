def fib(times):
    n=0
    a,b = 0,1
    while n<times:
        temp = yield b
        print(temp)
        a,b = b,a+b
        n+=1

f = fib(5)
print(f.__next__())
print(f.send("Se7eN_HOU"))
print(f.send("Se7eN"))
print(next(f))
print(f.__next__())