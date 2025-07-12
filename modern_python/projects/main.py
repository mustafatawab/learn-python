# prev: int = 1
current: int = 1
next:int = 2

# m:int = 1

multi:list[int] = []
for x in range(1 , 11):
    print(x , end=' ')
    # m *= x
    m = x * next    
    multi.append(m)
    current = next
    next = current + 1

print(multi)