def fibonacci(n):
    a, b = 0, 1
    while a < n:
        yield a #lagrar upp tal genom att returna talen
        a, b = b, a + b
        
for i in fibonacci(1000): #loppar igenom alla talen som yieldats.
    print(i)
