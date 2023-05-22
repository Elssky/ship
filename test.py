import random
def sort_list(lst):
    zeros = [i for i in range(len(lst)) if lst[i] == 0]
    zeros.append(len(lst))
    res = []
    start = 0
    end = zeros[0]
    res += sorted(lst[start:end])
    for i in range(len(zeros)-1):      
        start = zeros[i]
        end = zeros[i+1]
            
        res += sorted(lst[start:end])
    return res

# lst = [3, 0, 2, 0, 1, 0, 4, 0, 5, 6, 7, 0, 8, 0, 9, 0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15, 0, 16, 0, 17, 0, 18, 0, 19, 0, 20, 0, 21, 0, 22, 0, 23, 0, 24, 0, 25, 0, 26, 0, 27, 0, 28]


lst = random.sample(range(50), 9)
result = [0 if i in lst else random.randint(1, 100) for i in range(50)]
print(result)
print(sort_list(result))


