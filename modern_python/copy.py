# import copy

list1 : list = [[1,2,3] , [3. , 9 , 2]]
# Shallow Copy  - By Reference 
shallow_copy = list1


shallow_copy[0].append(12)

print(shallow_copy)
print(list1)


# deep copy - copy of the original list. 
list2 : list = [ [12,12,34] ,  [9 , 8 , 7]]
deep_copy = list2[:]

deep_copy.append(900)

print(deep_copy)
print(list2)